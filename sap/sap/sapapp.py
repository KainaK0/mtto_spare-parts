import win32com.client
from enum import Enum
from typing import final,Any
#from builtins import classmethod

class SapGui():
    # _SapGuiAuto = win32com.client.GetObject("SAPGUI")
    # servidor: ServidorSap = ServidorSap.QAS.value
    # from_saplogon: bool = False
    system: dict[str] = {'prd':"PRD [MINSUR]", 'qas':"QAS MINSUR"}
    def __init__(self) -> None:
        pass

    @classmethod
    def start(cls) -> None:
        cls.login()
        cls.updateStatus()
        print(cls.transaction)

    @classmethod
    def login(cls) -> None:
        try:
            cls.SapGuiAuto = win32com.client.GetObject('SAPGUI')
        except:
            "Open saplogon app"
        
        cls.app = cls.SapGuiAuto.GetScriptingEngine

        if cls.app.children.count == 0:
            
            cls.app.openconnection(cls.system.get('qas'), True)
            cls.userinfo()
            cls.updateListPaths()
        elif cls.app.children.count > 0 and cls.app.children(0).children(0).info.screennumber == 20:
            cls.userinfo()


    @classmethod
    def connection(cls, connection: int = 0, session: int = 0) -> Any:
        cls.app = cls._SapGuiAuto.GetScriptingEngine
        # if cls.from_saplogon == False:
        #     cls.conn = cls._application.Children(0)
        # else:
        #     cls.conn = cls._application.OpenConnection(cls.servidor, True)
        # return cls.conn

    @classmethod
    def userinfo(cls, user:str = "jcallomamanb", password:str = "pruebas011", connection:int = 0, session:int = 0) -> None: ## I need to change it for a login experience
        cls.app.findById(f"con[{connection}]/ses[{session}]/wnd[0]/usr/txtRSYST-BNAME").text = user
        cls.app.findById(f"con[{connection}]/ses[{session}]/wnd[0]/usr/pwdRSYST-BCODE").text = password
        cls.app.findById(f"con[{connection}]/ses[{session}]/wnd[0]").sendVKey(0)

    @classmethod
    def go2tx(cls, tx: str, connection: int = 0, session: int = 0):
        cls.app.findById(f"con[{connection}]/ses[{session}]/wnd[0]/tbar[0]/okcd").text = "/n" + tx
        cls.app.findById(f"con[{connection}]/ses[{session}]/wnd[0]/tbar[0]/btn[0]").press()

    @classmethod
    def updateStatus(cls, connection: int = 0, session: int = 0) -> str:
        info = cls.app.findById(f"con[{connection}]/ses[{session}]").info
        cls.window_status = str(cls.app.findById(f"con[{connection}]/ses[{session}]/wnd[0]").text)
        cls.user = str(info.user)
        cls.transaction = str(info.transaction)
        cls.system_name = str(info.systemname)
        cls.client = str(info.client)
        cls.screen_number = str(info.screennumber)

    @classmethod
    def close(cls) -> None:
        pass

    @classmethod    
    def enter(cls, times: int = 1, connection: int = 0, session: int = 0) -> None:
        for i in range(times):
            cls.app.findById(f"con[{connection}]/ses[{session}]/wnd[0]").sendVKey(0)
    
    @classmethod
    def updateListPaths(cls) -> None:
        number_conn = int(cls.app.children.count)
        list_path_id = {}
        cls.conn_list = {}
        for num_conn in range(0, number_conn):
            session_list_id = {}
            number_sess = int(cls.app.children(num_conn).children.count)
            for num_sess in range(0,number_sess):
                session_list_id[num_sess]= {
                    'name': cls.app.children(num_conn).children(num_sess).name,
                    'id': cls.app.children(num_conn).children(num_sess).id,
                    'systemname': cls.app.children(num_conn).children(num_sess).info.systemname
                }
            list_path_id[num_conn] = {
                'name': cls.app.children(num_conn).name,
                'id': cls.app.children(num_conn).id,
                'systemname': session_list_id[0]['systemname'],
                #'sessions': session_list_id
            }
            list_path_id[num_conn]['sessions'] = session_list_id

            cls.conn_list = list_path_id


    @classmethod
    def skipWindows(cls, screen_number: str, connection: int = 0, session: int = 0) -> None:
        session0 = cls.app.findById(f"con[{connection}]/ses[{session}]")
        cls.updateStatus()
        if cls.screen_number == screen_number:
            while int(session0.children.count) > 1:
                cls.app.findById(f"con[{connection}]/ses[{session}]/wnd[1]").sendVKey(0)
            print("go out of windows information")
    

    