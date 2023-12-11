from sap.sap import SapGui
from sap.data import table2dataframe
import pandas as pd
import pyperclip
import os

class mm60tx(SapGui):
    rute = r"C:\Users\jcallomamanib\Minsur S.A\Planeamiento Mtto - Planta Concentradora - Documentos\03_materiales\01_data_sap"
    file_input_name = r"mm60.txt"
    file_output_name = r"mm60.csv"
    file_input = os.path.join(rute,file_input_name)
    file_output = os.path.join(rute,file_output_name)
    data:pd.DataFrame = pd.DataFrame
    # sap_app:SapGui
    def __init__(self, sap_app:SapGui) -> None:
        super().__init__()
        self.sap_app = sap_app

    @classmethod
    def download(cls, list_material:list[str], conn:int = 0, sess:int = 0) -> None:
        # cls.connection()
        # cls.login()
        # cls.updateStatus()

        cls.app = cls.sap_app
        cls.go2tx(connection=conn,session=sess,tx="MM60")

        cls.app.findById(f"con[{conn}]/ses[{sess}]/wnd[0]/mbar/menu[2]/menu[0]/menu[0]").select()
        cls.app.findById(f"con[{conn}]/ses[{sess}]/wnd[1]/usr/txtV-LOW").text = "/BDMM60"  #"/BDIW29"
        cls.app.findById(f"con[{conn}]/ses[{sess}]/wnd[1]/usr/txtENAME-LOW").text = "JCALLOMAMANB" #"JCALLOMAMANB"
        cls.app.findById(f"con[{conn}]/ses[{sess}]/wnd[1]/tbar[0]/btn[8]").press()

        cls.app.findById(f"con[{conn}]/ses[{sess}]/wnd[0]/usr/ctxtMS_MATNR-LOW").text = "" 

        cls.app.findById(f"con[{conn}]/ses[{sess}]/wnd[0]/usr/btn%_MS_MATNR_%_APP_%-VALU_PUSH").press() # Abrir material masivo
        cls.app.findById(f"con[{conn}]/ses[{sess}]/wnd[1]/tbar[0]/btn[16]").press()
        pyperclip.copy('\r\n'.join(list_material))
        cls.app.findById(f"con[{conn}]/ses[{sess}]/wnd[1]/tbar[0]/btn[24]").press() # Pegar lista de materiales
        cls.app.findById(f"con[{conn}]/ses[{sess}]/wnd[1]/tbar[0]/btn[8]").press() # Aceptar lista masiva de materiales
        cls.app.findById(f"con[{conn}]/ses[{sess}]/wnd[0]/usr/ctxtMS_WERKS-LOW").text = "" # Centro

        cls.app.findById(f"con[{conn}]/ses[{sess}]/wnd[0]/usr/btn%_MS_WERKS_%_APP_%-VALU_PUSH").press() # Abrir centro masivo
        cls.app.findById(f"con[{conn}]/ses[{sess}]/wnd[1]/tbar[0]/btn[16]").press()
        pyperclip.copy('\r\n'.join(['JP11','JP14']))
        cls.app.findById(f"con[{conn}]/ses[{sess}]/wnd[1]/tbar[0]/btn[24]").press() # Pegar lista de centros
        cls.app.findById(f"con[{conn}]/ses[{sess}]/wnd[1]/tbar[0]/btn[8]").press() 
        cls.app.findById(f"con[{conn}]/ses[{sess}]/wnd[0]/usr/chkBEWFLG").selected = True

        cls.app.findById(f"con[{conn}]/ses[{sess}]/wnd[0]/tbar[1]/btn[8]").press() # EJECUTAR TRANSACCION

        cls.app.findById(f"con[{conn}]/ses[{sess}]/wnd[0]/tbar[1]/btn[33]").press() # Select a variant

        rowCount = cls.app.findById(f"con[{conn}]/ses[{sess}]/wnd[1]/usr/ssubD0500_SUBSCREEN:SAPLSLVC_DIALOG:0501/cntlG51_CONTAINER/shellcont/shell").rowCount

        for i in range(rowCount):
            if cls.app.findById(f"con[{conn}]/ses[{sess}]/wnd[1]/usr/ssubD0500_SUBSCREEN:SAPLSLVC_DIALOG:0501/cntlG51_CONTAINER/shellcont/shell").getCellValue(i,"VARIANT") == "BDMM60":
                cls.app.findById(f"con[{conn}]/ses[{sess}]/wnd[1]/usr/ssubD0500_SUBSCREEN:SAPLSLVC_DIALOG:0501/cntlG51_CONTAINER/shellcont/shell").selectedRows = f"{i}"
                cls.app.findById(f"con[{conn}]/ses[{sess}]/wnd[1]/usr/ssubD0500_SUBSCREEN:SAPLSLVC_DIALOG:0501/cntlG51_CONTAINER/shellcont/shell").doubleClick(i,"VARIANT")
                # cls.app.findById(f"con[{conn}]/ses[{sess}]/wnd[1]/tbar[0]/btn[0]").press()
                break

        cls.app.findById(f"con[{conn}]/ses[{sess}]/wnd[0]/mbar/menu[0]/menu[3]/menu[2]").select()
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