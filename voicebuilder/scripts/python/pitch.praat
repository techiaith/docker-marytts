# pitch.praat <wavfile.wav>  75 300” 
form Provide arguments
  sentence wavFile tmp.wav
  real minPitch 75
  real maxPitch 600
endform

pitchFile$ = "tmp.Pitch"
pointpFile$ = "tmp.PointProcess"

wav = Read from file... 'wavFile$'

# Remove DC offset, if present:
Subtract mean

# First, low-pass filter the speech signal to make it more robust against noise
# (i.e., mixed noise+periodicity regions treated more likely as periodic)
sound = Filter (pass Hann band)... 0 1000 100

# check for available Pitch file:
if fileReadable(pitchFile$)
  pitch = Read from file... 'pitchFile$'
else
  # determine pitch curve:
  noprogress To Pitch... 0 minPitch maxPitch
  pitch = selected()
endif

# Get some debug info: 
min_f0 = Get minimum... 0 0 Hertz Parabolic
max_f0 = Get maximum... 0 0 Hertz Parabolic

# And convert to pitch marks:
plus sound
noprogress To PointProcess (cc)
pp = selected()

# convert pitch contour and pitch marks to PitchTier for easier access:
plus pitch
pt = To PitchTier

# Fill in 100 Hz pseudo-pitchmarks in unvoiced regions:
fill_f0 = 100 ; define constant

# get v/uv intervals:
select pp
# TODO tweak parameters?
tg = To TextGrid (vuv)... 0.02 0.01
# sanity check: are there even any unvoiced intervals?
ni = Get number of intervals... 1
if ni == 1
  i$ = Get label of interval... 1 1
  if i$ == "V"
    select pp
    goto writepp
  endif
endif
it = Extract tier... 1
uv = Down to TableOfReal... U

# iterate over uv intervals (two passes to avoid concurrent modification):
select pp
for row to Object_'uv'.nrow
  # get the fill start time:
  uv_start = Object_'uv'[row,"Start"]
  prev_pm_idx = Get low index... uv_start
  is_first_pm = prev_pm_idx == 0
  if is_first_pm
    fill_start = uv_start
  else
    prev_pm_time = Get time from index... prev_pm_idx
    prev_f0 = Object_'pt'[prev_pm_idx]
    fill_start = prev_pm_time + 1 / fill_f0
  endif

  # get the fill end time:
  uv_end = Object_'uv'[row,"End"]
  next_pm_idx = Get high index... uv_end
  is_last_pm = next_pm_idx > Object_'pt'.nx
  if is_last_pm
    fill_end = uv_end
  else
    next_pm_time = Get time from index... next_pm_idx
    next_f0 = Object_'pt'[next_pm_idx]
    fill_end = next_pm_time - 1 / fill_f0
  endif

  # adjust fill start and end times so that fill pitchmarks are centered in fill region:  
  fill_length = fill_end - fill_start
  fill_pm_remainder = fill_length mod (1 / fill_f0)
  if is_first_pm
    fill_start += fill_pm_remainder
  elsif is_last_pm
    fill_end -= fill_pm_remainder
  else
    fill_start += fill_pm_remainder / 2
    fill_end -= fill_pm_remainder / 2
  endif

  # store values
  fill_start_'row' = fill_start
  fill_end_'row' = fill_end
endfor

# do the fill:
for row to Object_'uv'.nrow
  time = fill_start_'row'
  while time <= fill_end_'row' + 1e-14 ; try to gracefully handle floating-point noise
    Add point... time
    time += 1 / fill_f0
  endwhile
endfor

label writepp
Write to short text file... 'pointpFile$'

# cleanup:
plus wav
plus sound
plus pitch
plus pt
plus pp
plus tg
nocheck plus it
nocheck plus uv
Remove
