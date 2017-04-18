import aiodns
import asyncio
import ipaddress
import pycares
import random

MC_SRV_PREFIX = "_minecraft._tcp."
LOOP = asyncio.get_event_loop()


class MCDNSResolver:
    def __init__(self):
        self._resolver = aiodns.DNSResolver(loop=LOOP)
    
    def _groupsort_ind_record(self, records, r):
        for i in range(len(records)):
            if records[i][0].priority is r.priority:
                records[i].append(r)
                return
            elif records[i][0].priority < r.priority:
                records.insert(i, [r])
                return
        records.append([r])


    def _groupsort_by_priority(self, records):
        ret = []
        for r in records:
            self._groupsort_ind_record(ret, r)
        return ret

    def _yield_weighted_random(self, records):
        total = 0
        for r in records:
            total += r.weight
        
        while total > 0:
            s = random.randint(1, total)
            for r in records:
                s -= r.weight
                if s <= 0:
                    total -= r.weight
                    yield r
                    break

    def _is_ip_address(self, addr):
        try:
            ipaddress.ip_address(addr)
            return True
        except ValueError:
            return False

    def _is_ip_6(self, addr):
        try:
            ipaddress.IPv6Address(addr)
            return True
        except ValueError:
            return False

    async def _recursive_cname_a_lookup(self, host, allow_6=True):
        try:
            cname = await self._resolver.query(host, 'CNAME')
            ag = self._recursive_cname_a_lookup(cname.cname, allow_6=allow_6)
            async for a in ag:
                yield a
        except aiodns.error.DNSError:
            pass

        if allow_6:
            try:
                aaaa_r = await self._resolver.query(host, 'AAAA')
                for aaaa in aaaa_r:
                    yield aaaa.host
            except aiodns.error.DNSError:
                pass

        a_r = await self._resolver.query(host, 'A')
        for a in a_r:
            yield a.host

    def split_domain_port(self, domain):
        spl = domain.rpartition(":")
        if spl[0] is '':
            return domain, -1
        else:
            return spl[0], int(spl[2])

    async def resolve(self, connection_string, allow_6=True, log=print):
        """
        Returns a generator which async generates ip - port pairs to join
        PEP 525
        """

        if log is None:
            def log(_):
                pass

        domain, port = self.split_domain_port(connection_string)

        if self._is_ip_address(domain):
            if not allow_6 and self._is_ip_6(domain):
                raise "ipv6 connection ip passed and ipv6 not allowed"
            if port is -1:
                port = 25565

            yield (domain, port)
            return

        yields = []

        def dedupe(ip, port):
            r = (ip, port)
            if not r in yields:
                yields.append(r)
                return True
            return False

        if port is -1:
            try:
                result = await self._resolver.query(MC_SRV_PREFIX + domain, 'SRV')
                rec_grps = self._groupsort_by_priority(result)
                for grp in rec_grps:
                    for rec in self._yield_weighted_random(grp):
                        host = rec.host
                        if not self._is_ip_address(host):
                            try:
                                results = self._recursive_cname_a_lookup(host, allow_6=allow_6)
                                async for res in results:
                                    result = (res, rec.port)
                                    if dedupe(*result):
                                        yield result
                            except aiodns.error.DNSError:
                                log("Attempted recursive lookup of srv with host '{}' failed, skipping".format(host))
                                continue
                        else:
                            if not allow_6 and _is_ip_6(host):
                                continue
                            
                            result = (res, rec.port)
                            if dedupe(*result):
                                yield res

            except aiodns.error.DNSError:
                pass

            port = 25565

        results = self._recursive_cname_a_lookup(domain, allow_6)
        async for result in results:
            res = (result, port)
            if dedupe(*res):
                yield res


