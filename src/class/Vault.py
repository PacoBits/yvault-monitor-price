from web3 import Web3,HTTPProvider
import time,json,os
from datetime import datetime
from dotenv import load_dotenv



class Vault:
    """

    Parameters
    ----------
    chainId : int (1,3)
        1 para red Mainnet y 3 para Ropsten
    claveprivada : str
        clave privada de la cuenta eth, o se pasa es parametro o el fichero para obtenerla
    cuenta : str
        clave privada de la cuenta eth, o se pasa es parametro o el fichero para obtenerla
    fichero : str
        fichero y ruta con la clave privada. O se pasa este parametro o se pasa la clave privada
    clave : str
        clave para abrir el fichero ene l que esta cifrada la clave privada

    Attributes
    ----------
    contratoresolver : str
        direccion del contrato del ENS Public Resolver 
    """
    def __init__(self, chainId ,vaultAddress):
        self.chainId=chainId
        self.vaultAddress=vaultAddress
        self.LoadEnv()
        self.LoadJsonVault()
        print (self.infura)
        self.w3=Web3(HTTPProvider(self.infura))
        self.erc20s = self.w3.eth.contract(address=self.vaultAddress, abi=self.ERC20_ABI)


    def LoadEnv(self):        
        load_dotenv()        
        if self.chainId==1:
            self.infura=os.getenv("INFURA")
        if self.chainId==3:
            self.infura=os.getenv("INFURA_ROPSTEN")            


    def LoadJsonFile(self,file):
        with open(file) as json_file:
            return json.load(json_file)

    def LoadJsonVault(self):
        if self.chainId==1:
            print('Contrato Mainnet')
            if (self.vaultAddress=='0x5f18C75AbDAe578b483E5F43f12a39cF75b973a9'):
                self.ERC20_ABI=self.LoadJsonFile('ABI/yvUSDC.json')
        else:
            if self.chainId==3:
                #TODO
                print('Contrato Ropsten')
                contract='0x12a0083531C904fe4ac490DF231c2e4e4403dB60'
                ERC20_ABI=self.LoadJsonFile('ABI/ETHRegistrarControllerRopsten.json')
            else:
                raise ValueError('No hay contrato para la red elegida')

    def pricePerShare(self):
        return self.erc20s.functions.pricePerShare().call()
    def decimals(self):
        return self.erc20s.functions.decimals().call()
    def HumanpricePerShare(self):
        return (self.pricePerShare()/10**(self.decimals()))      
    def Symbol(self):
        return self.erc20s.functions.symbol().call()  












