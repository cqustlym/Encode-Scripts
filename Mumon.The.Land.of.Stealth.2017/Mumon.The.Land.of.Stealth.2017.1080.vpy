import vapoursynth as vs
import awsmfunc as awf
import kagefunc as kgf
from vsutil import *
import adptvgrnMod as adp
import havsfunc as haf
import pterfunc as ptf
import vardefunc as vaf
import adptvgrnMod as agm
core = vs.core

# 0 Encode Flag
source_clip_path = r'F:\xxx\REMUX\Mumon.The.Land.of.Stealth.2017.BluRay.1080p.DTS-HD.MA.5.1.AVC.REMUX-FraMeSToR_Video01.UND.dgi'  # The path of source clip
encode_clip_path = r'Mumon- The Land of Stealth [2017] 1080p.dgi'  # The path of encode clip
target_clip_path = [r'Target', 'Mumon.The.Land.of.Stealth.2017.1080p.BluRay.x264.DTS-WiKi.mkv']  # First is The path of target clip and the second is the target clip's name
target_clips_path = {}  # For multiple clips,keys is the encode group and value is the path {"Handjob":r"/root/H.mkv"}
test_folder = r'F:\xxx\test\crf'  # The path of the test encodes
sample_extract = False  # True if you want to extract sample clip
sample_comparison = True  # True if you want to compare sample clip
encode_comparison = True  # True if you want to make a source vs encode
nvidia = True  # True if you have an nvidia video card

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

src = core.std.Crop(clip=src, top=138, bottom=138, left=0, right=0)  # Modify it with the even pixels to crop!
clip = depth(src, 16)

# 2 Filtering

# 2.1 Dirty lines & Borders
fix_borders = False
if fix_borders:
    fixed = awf.FixBrightnessProtect2(clip, row=[], adj_row=[], column=[], adj_column=[])
    fixed = awf.FillBorders(clip=clip, top=0, left=0,
                            right=0,
                            bottom=0)  # For lazy people who don't bother to fix them
    fixed = awf.bbmod(clip, top=0, bottom=0, left=0, right=0, thresh=0, blur=0)
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
    debandmask = ptf.debandmask(resized)
    luma_mask = y.std.Binarize(40000).std.Invert()
    luma_mask1 = y.std.Binarize(8000)
    edge_mask = kgf.retinex_edgemask(resized).std.Binarize(3200).std.Minimum().std.Deflate()
    filtered = ptf.DebandReader(resized, 'Mumon.The.Land.of.Stealth.2017.csv', mask=[debandmask,luma_mask,edge_mask,luma_mask1])
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
    # com = core.std.Interleave([rescale, filtered])
    # com.set_output()

    # Deband test
    # resized.set_output()
    # y = get_y(resized)
    # debandmask = ptf.debandmask(resized)
    # luma_mask = get_y(resized).std.Binarize(40000).std.Invert()
    # luma_mask1 = get_y(resized).std.Binarize(8000)
    # edge_mask = kgf.retinex_edgemask(resized).std.Binarize(3200).std.Minimum().std.Deflate()
    # filtered = ptf.DebandReader(resized, 'Mumon.The.Land.of.Stealth.2017.csv', mask=[debandmask,luma_mask,edge_mask,luma_mask1])
    # filtered.set_output(index=1)
    # debandmask.set_output(index=2)
    # luma_mask.set_output(index=3)
    # edge_mask.set_output(index=4)

    # Mask test
    # resized.set_output()
    # mask1 = kgf.retinex_edgemask(resized).std.Binarize(8000).std.Minimum().std.Deflate()
    # mask2= get_y(resized).std.Binarize(8000)
    # # mask3 = get_y(resized).std.Binarize(27000).std.Invert()
    # # mask1.set_output(index=1)
    # mask2.set_output(index=2)
else:
    filtered = depth(filtered, 8)
    if sample_extract is False and encode_comparison is False:
        filtered.set_output()

# 3 Sample Extract & Comparison
if sample_extract:
    filtered = awf.FrameInfo(filtered,
                             'Filtered') if sample_comparison else filtered  # Tag original frameinfo if compare sample
    # extract = ptf.banding_extract(filtered, 'Mumon.The.Land.of.Stealth.2017.csv')
    # source = ptf.banding_extract(depth(resized,8), 'Mumon.The.Land.of.Stealth.2017.csv')

    # source = awf.SelectRangeEvery(depth(resized,8), every=3000, length=50, offset=662) + ptf.banding_extract(depth(resized,8), 'Mumon.The.Land.of.Stealth.2017.csv')
    # extract = awf.SelectRangeEvery(filtered, every=3000, length=50, offset=662) + ptf.banding_extract(filtered, 'Mumon.The.Land.of.Stealth.2017.csv')  # Modify it with the length to extract!
    if sample_comparison:
        comparison = ptf.InterleaveDir(folder=test_folder, PrintInfo=True, first=[source,extract], repeat=True)
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
    # awf.ScreenGen(comparison, r'comparsion\Mumon.The.Land.of.Stealth.2017\tmp', 'a',ptf.multy([126890],4)) # take screenshots
    comparison.set_output()
