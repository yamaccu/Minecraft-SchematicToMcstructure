from asyncio.windows_events import NULL
import amulet
from amulet.level.formats.mcstructure import MCStructureFormatWrapper
import tkinter
from tkinter import messagebox
from tkinter import filedialog
import logging
import sys

log = logging.getLogger(__name__)
tk = tkinter
tk.Tk().withdraw()

type = [('Legacy Schematic file','*.schematic')]
importpath = tk.filedialog.askopenfilename(filetypes = type)
log.info(importpath)

if importpath == "":
    tk.messagebox.showwarning('メッセージ', 'ファイルを読み込みできませんでした')
    sys.exit()

level = amulet.load_level(importpath)
selection =  level.bounds(level.dimensions[0])
#log.info(selection)

index1 = importpath.rfind(r'/')
index2 = importpath.rfind('.')
filename = importpath[index1+1:index2]
exportpath = importpath[0:index1] + "\\" + filename + ".mcstructure"
#log.info(index1)
#log.info(index2)
#log.info(exportpath)
#log.info(filename)
wrapper = MCStructureFormatWrapper(exportpath)

try:
    wrapper.create_and_open("bedrock", [1, 19, 0], selection, False)
except:
    tk.messagebox.showwarning('メッセージ', '同名の.mcstructureファイルが存在します')
    sys.exit()
wrapper_dimension = wrapper.dimensions[0]
#log.info(chunk_count)
#log.info(selection.chunk_locations())
for (cx, cz) in selection.chunk_locations():
    chunk = level.get_chunk(cx, cz, level.dimensions[0])
    wrapper.commit_chunk(chunk, wrapper_dimension)
wrapper.save()
wrapper.close()
tk.messagebox.showinfo('メッセージ', '完了しました。')
