import amulet
from amulet.level.formats.mcstructure import MCStructureFormatWrapper
import wx
import logging
import sys

log = logging.getLogger(__name__)

app = wx.App()
with wx.FileDialog(
    None,
    'Select Schematic File',
    wildcard="|".join(
        [
            "Legacy Schematic file (*.schematic)|*.schematic",
            "All files (*.construction;*.mcstructure;*.schematic)|*.construction;*.mcstructure;*.schematic",
        ]),
    style=wx.FD_OPEN) as dialog:
    if dialog.ShowModal() == wx.ID_OK:
        importpath = dialog.GetPaths()[0]
    else:
        sys.exit()

level = amulet.load_level(importpath)
selection =  level.bounds(level.dimensions[0])
#log.info(selection)

index1 = importpath.rfind("\\")
index2 = importpath.rfind(".")
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
    box=wx.MessageDialog(None,'同名の.mcstructureファイルが存在します','',wx.OK)
    box.ShowModal()
    sys.exit()
wrapper_dimension = wrapper.dimensions[0]
#log.info(chunk_count)
#log.info(selection.chunk_locations())
for (cx, cz) in selection.chunk_locations():
    chunk = level.get_chunk(cx, cz, level.dimensions[0])
    wrapper.commit_chunk(chunk, wrapper_dimension)
wrapper.save()
wrapper.close()
box=wx.MessageDialog(None,'完了しました','',wx.OK)
box.ShowModal()

