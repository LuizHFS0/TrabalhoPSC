import customtkinter as ctk

from cores import *

class VerTreinos(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(bg_color=FUNDO)
        
        # Frame do centro
        centro = ctk.CTkFrame(self, fg_color=FUNDO_CARD, height=600, width=800)
        centro.place(relx=0.5, rely=0.5, anchor="center")
        centro.pack_propagate(False)
        
        topo = ctk.CTkFrame(centro, height=70, fg_color="transparent")
        topo.pack(fill="x")
        
        ctk.CTkLabel(topo, text="Treinos de (Nome do aluno)", font=("Inter", 20, "bold")).place(anchor="center", relx=0.3, y=30)
        