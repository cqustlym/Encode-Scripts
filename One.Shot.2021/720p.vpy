import vapoursynth as vs
import awsmfunc as awf
# import btpfunc as btf
from vsutil import depth
import kagefunc as kgf
from adptvgrnMod import adptvgrnMod

core = vs.core

src = core.lsmas.LWLibavSource('src/video.h264', format='YUV420p16').std.CropRel(top=60, bottom=60)
clip = awf.zresize(src, preset=720, kernel='spline36')
clipf = clip

### Debanding
db = core.neo_f3kdb.Deband(clipf, range=16, y=100, preset='luma/nograin')
gr = adptvgrnMod(db, size=1, grain_chroma=False, static=False)
clipf = awf.ReplaceFrames(clipf, gr, mappings='[0 286] [604 786]')

db = core.neo_f3kdb.Deband(clipf, range=4, y=70, preset='luma/nograin')
gr = adptvgrnMod(db, size=1, grain_chroma=False, static=False)
mm = awf.LumaMaskMerge(clipf, gr, threshold=70, invert=False, scale_inputs=True)
em = kgf.retinex_edgemask(clipf)
mm = core.std.MaskedMerge(mm, clipf, em)
clipf = awf.ReplaceFrames(clipf, mm, mappings='[62434 62670]')

db = core.neo_f3kdb.Deband(clipf, range=8, y=80, preset='luma/nograin')
gr = adptvgrnMod(db, size=1, grain_chroma=False, static=False)
mm = awf.LumaMaskMerge(clipf, gr, threshold=170, invert=False, scale_inputs=True)
em = kgf.retinex_edgemask(clipf)
mm = core.std.MaskedMerge(mm, clipf, em)
clipf = awf.ReplaceFrames(clipf, mm, mappings='[9085 9444]')

#db = core.neo_f3kdb.Deband(clipf, range=8, y=80, preset='luma/nograin')
#gr = adptvgrnMod(db, size=1, grain_chroma=False, static=False)
mm = awf.LumaMaskMerge(clipf, gr, threshold=120, invert=False, scale_inputs=True)
em = kgf.retinex_edgemask(clipf)
mm = core.std.MaskedMerge(mm, clipf, em)
clipf = awf.ReplaceFrames(clipf, mm, mappings='[70588 71234]')

#db = core.neo_f3kdb.Deband(clipf, range=8, y=80, preset='luma/nograin')
#gr = adptvgrnMod(db, size=1, grain_chroma=False, static=False)
mm = awf.LumaMaskMerge(clipf, gr, threshold=90, invert=False, scale_inputs=True)
em = kgf.retinex_edgemask(clipf)
mm = core.std.MaskedMerge(mm, clipf, em)
clipf = awf.ReplaceFrames(clipf, mm, mappings=(
    '[28677 29107] [29629 29653] [30883 30915] [37980 38073] [62359 62433] [68616 68683] '
    '[68765 69407] [72454 73120] [86809 86964] [87129 87376] [87488 87558] [87720 88008]'
))

#db = core.neo_f3kdb.Deband(clipf, range=8, y=80, preset='luma/nograin')
#gr = adptvgrnMod(db, size=1, grain_chroma=False, static=False)
mm = awf.LumaMaskMerge(clipf, gr, threshold=25, invert=True, scale_inputs=True)
em = kgf.retinex_edgemask(clipf)
mm = core.std.MaskedMerge(mm, clipf, em)
clipf = awf.ReplaceFrames(clipf, mm, mappings='[13603 13781] [29129 29163] [94552 94993] [105895 105934] [105954 106138] [114721 114729]')

#db = core.neo_f3kdb.Deband(clipf, range=8, y=80, preset='luma/nograin')
#gr = adptvgrnMod(db, size=1, grain_chroma=False, static=False)
mm = awf.LumaMaskMerge(clipf, gr, threshold=80, invert=True, scale_inputs=True)
em = kgf.retinex_edgemask(clipf)
mm = core.std.MaskedMerge(mm, clipf, em)
clipf = awf.ReplaceFrames(clipf, mm, mappings='[102142 102279] [120321 120431] [121146 121256] [121734 121848] [133420 134506]')

#db = core.neo_f3kdb.Deband(clipf, range=8, y=80, preset='luma/nograin')
#gr = adptvgrnMod(db, size=1, grain_chroma=False, static=False)
mm = awf.LumaMaskMerge(clipf, gr, threshold=150, invert=True, scale_inputs=True)
em = kgf.retinex_edgemask(clipf)
mm = core.std.MaskedMerge(mm, clipf, em)
clipf = awf.ReplaceFrames(clipf, mm, mappings='[108405 108519] [110252 110335] [110655 111327] [127442 129744]')

#db = core.neo_f3kdb.Deband(clipf, range=8, y=80, preset='luma/nograin')
#gr = adptvgrnMod(db, size=1, grain_chroma=False, static=False)
mm = awf.LumaMaskMerge(clipf, gr, threshold=185, invert=True, scale_inputs=True)
em = kgf.retinex_edgemask(clipf)
mm = core.std.MaskedMerge(mm, clipf, em)
clipf = awf.ReplaceFrames(clipf, mm, mappings='[111370 112083]')

#db = core.neo_f3kdb.Deband(clipf, range=8, y=80, preset='luma/nograin')
#gr = adptvgrnMod(db, size=1, grain_chroma=False, static=False)
mm = awf.LumaMaskMerge(clipf, gr, threshold=120, invert=True, scale_inputs=True)
em = kgf.retinex_edgemask(clipf)
mm = core.std.MaskedMerge(mm, clipf, em)
clipf = awf.ReplaceFrames(clipf, mm, mappings='[130264 130717]')

# Credit 916-1621 134607-139199

#clip = depth(clip, 8, dither_type='error_diffusion')
clipf = depth(clipf, 8, dither_type='error_diffusion')

#clip = btf.FFInfo(clip, text='Source')
#clipf = btf.FFInfo(clipf, text='Filtered')

#out = core.std.Interleave([clip, clipf])
#out.set_output()

clipf.set_output()
