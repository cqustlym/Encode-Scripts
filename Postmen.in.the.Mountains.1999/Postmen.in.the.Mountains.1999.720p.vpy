import vapoursynth as vs
import awsmfunc as awf
import kagefunc as kgf
from vsutil import *
import adptvgrnMod as adp
import havsfunc as haf
import pterfunc as ptf
import vardefunc as vaf

core = vs.core

# 0 Encode Flag
source_clip_path = r'F:\XXX\REMUX\12488 PID 1011.dgi'  # The path of source clip
encode_clip_path = r'Postmen in the Mountains [1999] 720p.mkv'  # The path of encode clip
target_clip_path = [r'usury', 'postmen.in.the.mountains.1999.720p.bluray.x264-usury.mkv']  # First is The path of target clip and the second is the target clip's name
target_clips_path = {}  # For multiple clips,keys is the encode group and value is the path {"Handjob":r"/root/H.mkv"}
test_folder = r'F:\xxx\test\crf'  # The path of the test encodes
sample_extract = False  # True if you want to extract sample clip
sample_comparison = True  # True if you want to compare sample clip
encode_comparison = True  # True if you want to make a source vs encode

# 0 Init
if target_clip_path[1]:
    target_clips_path[target_clip_path[0]] = target_clip_path[1]

# 1 Import Source And Crop
if source_clip_path.endswith('.dgi'):
    src = core.dgdecodenv.DGSource(source_clip_path)
else:
    src = core.lsmas.LWLibavSource(source_clip_path)
if encode_comparison:
    if encode_clip_path.endswith('.dgi'):
        encode = core.dgdecodenv.DGSource(encode_clip_path)
    else:
        encode = core.lsmas.LWLibavSource(encode_clip_path)
else:
    encode = False
if encode_comparison and target_clips_path:
    target = [[i, core.dgdecodenv.DGSource(target_clips_path[i]) if target_clips_path[i].endswith('.dgi') else core.lsmas.LWLibavSource(target_clips_path[i])] for i in
              target_clips_path.keys()]
else:
    target = False
src = core.vivtc.VFM(clip=src, order=0, mode=0)
src = core.vivtc.VDecimate(src)
src = core.std.Crop(clip=src, top=22, bottom=22, left=2, right=2)  # Modify it with the even pixels to crop!
clip = depth(src, 16)
# 2 Filtering

# 2.1 Dirty lines & Borders
fix_borders = True
if fix_borders:
    fixed = awf.FillBorders(clip=clip,top=2,bottom=2,planes=[1,2])
    fixed = awf.FixBrightnessProtect2(fixed, column=[0], adj_column=[23])
    fixed = awf.FixBrightnessProtect2(fixed, column=[clip.width-1], adj_column=[23])
    # fixed = awf.FillBorders(clip=fixed,left=1,right=1,planes=[1,2])
    fixed = awf.bbmod(fixed, top=0, bottom=0, left=1, right=1, blur=999)
    fixed = ptf.dlreder(fixed,'dirty_lines.csv')
else:
    fixed = clip

# 2.2 Resized
resize = True
if resize:
    resized = awf.zresize(fixed, preset=720)
else:
    resized = fixed

# 2.3 Deband & Deblock
deband = True
if deband:
    y = get_y(resized)
    lumamask = y.std.Binarize(55000).std.Invert().std.Deflate()
    resized.set_output()
    filtered = ptf.DebandReader(resized, 'Postmen.in.the.Mountains.1999.csv',mask=[lumamask])
else:
    filtered = resized

# 2.4 Out!
test = False
if test:
    '''Any test here'''
    # Gama test area
    # gama = awf.autogma(filtered)
    # gama.set_output()
    # filtered.set_output(index=1)

    # Upscale check
    # downscale = awf.zresize(filtered, preset=720)
    # rescale = awf.zresize(downscale, preset=1080)
    # rescale = awf.FrameInfo(rescale, 'upscale')
    # rescale.set_output(index=0)
    # filtered.set_output(index=1)

    # mask test
    y = get_y(resized)
    lumamask = y.std.Binarize(55000).std.Invert().std.Deflate()
    resized.set_output()
    filtered = ptf.DebandReader(resized, 'Postmen.in.the.Mountains.1999.csv',mask=[lumamask])
    filtered.set_output(index=1)
else:
    filtered = depth(filtered, 8)
    if sample_extract is False and encode_comparison is False:
        filtered.set_output()

# 3 Sample Extract & Comparison
if sample_extract:
    filtered = awf.FrameInfo(filtered,
                             'Filtered') if sample_comparison else filtered  # Tag original frameinfo if compare sample
    extract = awf.SelectRangeEvery(filtered, every=3000, length=50, offset=1600)
    # extract = awf.SelectRangeEvery(filtered, every=3000, length=50, offset=1600) + ptf.banding_extract(filtered, 'Postmen.in.the.Mountains.1999.csv')  # Modify it with the length to extract!
    if sample_comparison:
        comparison = ptf.InterleaveDir(folder=test_folder, PrintInfo=True, first=[extract], repeat=True)
        depth(comparison, 8).set_output()
    else:
        depth(extract, 8).set_output()

# 4 Source VS Encode
if encode_comparison:
    src = awf.FrameInfo(src, 'Source') if not resize else awf.FrameInfo(depth(awf.zresize(clip, preset=720), 8),
                                                                        'Source')
    filtered = awf.FrameInfo(filtered, 'Filtered')
    encode = awf.FrameInfo(encode, 'Encode')
    comparison_list = [src, filtered, encode]
    if target:
        target = [awf.FrameInfo(i[1], i[0]) for i in target]
        comparison_list.extend(target)
    comparison = core.std.Interleave(comparison_list)
    # awf.ScreenGen(comparison, r'comparsion\Postmen.in.the.Mountains.1999', 'a',ptf.multy([63691,124096,106613,112610,7649,4867,41949,68307,76835,79841,94173,97739,124792,13932,78619],4)) # take screenshots
    comparison.set_output()
