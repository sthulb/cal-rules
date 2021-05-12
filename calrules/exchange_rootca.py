from requests import adapters

class ExchangeRootCA(adapters.HTTPAdapter):
    ca_cert: str

    def cert_verify(self, conn, url, verify: str, cert):
        verify = self.ca_cert
        return super().cert_verify(conn=conn, url=url, verify=verify, cert=cert)
