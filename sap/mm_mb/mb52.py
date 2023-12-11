from sap.pysap.sap import SapGui
from appsap.pysap.data import table2dataframe
import pandas as pd
import pyperclip
import os

class mb52tx(SapGui):
    rute = r"C:\Users\jcallomamanib\Minsur S.A\Planeamiento Mtto - Planta Concentradora - Documentos\03_materiales\01_data_sap"
    file_input_name = r"mb52.txt"
    file_output_name = r"mb52.csv"
    file_input = os.path.join(rute,file_input_name)
    file_output = os.path.join(rute,file_output_name)
    data:pd.DataFrame = pd.DataFrame

    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def download(cls,list_material:list[str], conn:int = 0, sess:int = 0) -> None:
        #cls.connection()
        cls.login()
        cls.updateStatus()

        cls.go2tx(connection=conn,session=sess,tx="MB52")

        cls.app.findById(f"con[{conn}]/ses[{sess}]/wnd[0]/mbar/menu[2]/menu[0]/menu[0]").select()
        cls.app.findById(f"con[{conn}]/ses[{sess}]/wnd[1]/usr/txtV-LOW").text = "/BDMB52_SU"  #"/BDIW29"
        cls.app.findById(f"con[{conn}]/ses[{sess}]/wnd[1]/usr/txtENAME-LOW").text = "JCALLOMAMANB" #"JCALLOMAMANB"
        cls.app.findById(f"con[{conn}]/ses[{sess}]/wnd[1]/tbar[0]/btn[8]").press()\

        # cls.app.findById(f"con[{conn}]/ses[{sess}]/wnd[0]/usr/ctxtMATNR-LOW").text = "" 
        cls.app.findById(f"con[{conn}]/ses[{sess}]/wnd[0]/usr/btn%_MATNR_%_APP_%-VALU_PUSH").press() # Abrir material masivo
        cls.app.findById(f"con[{conn}]/ses[{sess}]/wnd[1]/tbar[0]/btn[16]").press()
        pyperclip.copy('\r\n'.join(list_material))
        cls.app.findById(f"con[{conn}]/ses[{sess}]/wnd[1]/tbar[0]/btn[24]").press() # Pegar lista de materiales
        cls.app.findById(f"con[{conn}]/ses[{sess}]/wnd[1]/tbar[0]/btn[8]").press() # Aceptar lista masiva de materiales
        cls.app.findById(f"con[{conn}]/ses[{sess}]/wnd[0]/usr/ctxtLGORT-LOW").text = ""
        cls.app.findById(f"con[{conn}]/ses[{sess}]/wnd[0]/usr/ctxtP_VARI").text = "/BDmb52_SU"
        cls.app.findById(f"con[{conn}]/ses[{sess}]/wnd[0]/tbar[1]/btn[8]").press()

        cls.app.findById(f"con[{conn}]/ses[{sess}]/wnd[0]/mbar/menu[0]/menu[1]/menu[2]").select()
        cls.app.findById(f"con[{conn}]/ses[{sess}]/wnd[1]/usr/subSUBSCREEN_STEPLOOP:SAPLSPO5:0150/sub:SAPLSPO5:0150/radSPOPLI-SELFLAG[0,0]").select()
        cls.app.findById(f"con[{conn}]/ses[{sess}]/wnd[1]/tbar[0]/btn[0]").press()
        cls.app.findById(f"con[{conn}]/ses[{sess}]/wnd[1]/usr/ctxtDY_PATH").text = cls.rute
        cls.app.findById(f"con[{conn}]/ses[{sess}]/wnd[1]/usr/ctxtDY_FILENAME").text = cls.file_input_name
        cls.app.findById(f"con[{conn}]/ses[{sess}]/wnd[1]/usr/ctxtDY_FILE_ENCODING").text = "4103"
        cls.app.findById(f"con[{conn}]/ses[{sess}]/wnd[1]/tbar[0]/btn[11]").press()

    @classmethod
    def read_raw_data(cls) -> pd.DataFrame:
        rawtx = pd.read_table(cls.file_input, header = None, lineterminator= '\n', encoding="utf-16le")
        return rawtx

    @classmethod
    def tranform2csv(cls) -> None:
        rawtx = cls.read_raw_data()
        cls.data = table2dataframe(rawtx)
        cls.data.to_csv(cls.file_output, index=False, encoding="utf-8-sig")