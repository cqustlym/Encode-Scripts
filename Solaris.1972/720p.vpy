import vapoursynth as vs
import awsmfunc as awf
from vsutil import depth 

core = vs.core
#core.num_threads = 6
core.max_cache_size = 4096

nld = core.lsmas.LWLibavSource('src_nld/Solaris.1972.REPACK.1080p.NLD.BluRay.REMUX.AVC.FLAC.2.0-rutracker_track1_[rus].avc', format='YUV420p16').std.CropRel(top=132, bottom=132)
nld = awf.zresize(nld, preset=720, kernel='spline36')

fra = core.lsmas.LWLibavSource('src_fra/video.h264', format='YUV420p16').std.CropRel(top=132, bottom=132)
fra = awf.zresize(fra, preset=720, kernel='spline36')
fra = nld[:181] + fra[:-12]

hybrid = core.std.ShufflePlanes((fra, nld, nld), [0, 1, 2], vs.YUV)
# 16bit patch (worked for my case) - https://github.com/zamlty/vapoursynth-matchhistogram/tree/16bit
clipf = core.matchhist.MatchHistogram(hybrid, nld, planes=0, raw=True)

frames = '[46715 47543] [48081 55129] [60054 60614] [66897 67079] [68169 68360] [82827 83591]'
#        '[76566 78179] [184870 186077] [166034 182220] [210682 211745]'
clipf = awf.ReplaceFrames(nld, clipf, mappings=frames)

clipf = depth(clipf, 8, dither_type='error_diffusion')
clipf.set_output()
