from urllib3 import connection
from requests import adapters

class ExchangeRootCA(adapters.HTTPAdapter):
  ca_cert: str

  def __init__(self, ca_cert: str):
    self.ca_cert = ca_cert

  class Root(adapters.HTTPAdapter):
    def cert_verify(self, conn, url, verify, cert):
      return super().cert_verify(conn=conn, url=url, verify="root-x509.cer", cert=cert)
