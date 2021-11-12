import vapoursynth as vs
import awsmfunc as awf
from vsutil import depth 

core = vs.core
core.num_threads = 6

nld = core.lsmas.LWLibavSource('src_nld/Solaris.1972.REPACK.1080p.NLD.BluRay.REMUX.AVC.FLAC.2.0-rutracker_track1_[rus].avc', format='YUV420p16').std.CropRel(top=132, bottom=132)
nld = awf.zresize(nld, preset=720, kernel='spline36')

fra = core.lsmas.LWLibavSource('src_fra/video.h264', format='YUV420p16').std.CropRel(top=132, bottom=132)
fra = awf.zresize(fra, preset=720, kernel='spline36')
fra = nld[:181] + fra[:-12]

nld = depth(nld, 8, dither_type='error_diffusion')
fra = depth(fra, 8, dither_type='error_diffusion')

clipf = core.std.ShufflePlanes((fra, nld, nld), [0, 1, 2], vs.YUV)
clipf = core.matchhist.MatchHistogram(clipf, nld, planes=0)
clipf = awf.ReplaceFrames(nld, clipf, mappings='[48321 48368] [48585 48680] [53889 53973] [54201 54296] [54369 54451] [54570 54581]')

clipf.set_output()
