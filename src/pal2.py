# -*- coding: utf-8 -*-
from pal_data import P as OLD
import re
sn,_,SONG = OLD['song']; tn,_,TH = OLD['theory']
en,_,EMO = OLD['emotion']; xn,_,TEX = OLD['texture']
gn,gb,GEN = OLD['genre']

def dedup(seq):
    out=[];seen=set()
    for x in seq:
        k=x.lower()
        if k not in seen: seen.add(k); out.append(x)
    return out

P={}

# ---- Emotions: flat, uncategorised. Real affective states only. ----
KEEP_HYPHEN=("Self-","Non-","World-","Free-","Near-","Post-","Pre-","Three-")
def tidy(w):
    if w.startswith(KEEP_HYPHEN) and w.count("-")==1: return w
    return w.replace("-"," ")
_emo=[tidy(w) for w in open("emo_final.txt").read().split("\n") if w.strip()]
_seen=set(); EMOW=[]
for w in _emo:
    k=w.lower()
    if k not in _seen: _seen.add(k); EMOW.append(w)
P['emotion']=("Emotions","One feeling, aimed at. The mixed states are usually the interesting ones.",
              None, sorted(EMOW,key=str.lower)[:1000])

# ---- Theory: theory concepts + song elements merged, chords split from voicings ----
CHORDS=["Major triad","Minor triad","Diminished triad","Augmented triad","Major seventh",
 "Dominant seventh","Minor seventh","Half-diminished","Fully diminished","Minor-major seventh",
 "Sixth chord","Ninth chord","Eleventh chord","Thirteenth chord","Add9","Sus2","Sus4",
 "Altered dominant","Slash chord","Power chord","Polychord","Hybrid chord","Triad",
 "Seventh chord","Extension","Chord","Passing chord","Neighbor chord","Borrowed chord",
 "Secondary dominant","Tritone substitution","Neapolitan sixth","Augmented sixth",
 "Italian sixth","French sixth","German sixth","Quartal harmony","Open fifth","Cluster",
 "Chord symbol","Figured bass","Diminished seventh","Suspended chord","Augmented eleventh",
 "Altered fifth","Flat ninth","Sharp ninth","Sixth-nine chord","Major ninth","Dominant ninth",
 "Minor ninth"]
VOICINGS=["Voicing","Inversion","First inversion","Second inversion","Third inversion",
 "Root position","Close position","Open position","Spread voicing","Drop 2","Drop 3",
 "Drop 2-4","Rootless voicing","Shell voicing","Quartal voicing","Quintal voicing",
 "Upper structure triad","Cluster voicing","Block chords","Four-way close","Voice leading",
 "Common tone","Smooth voice leading","Contrary voice leading","Voicing spread",
 "Register spacing","Wide voicing","Tight voicing","Doubling","Omitted fifth","Omitted root",
 "Guide tones","Left-hand voicing","Piano voicing","Guitar voicing","Orchestral spacing",
 "Divisi","Closed harmony","Open harmony","Parallel voicing","Planing"]
def strip(src,*rm):
    kill={x.lower() for g in rm for x in g}
    return [w for w in src if w.lower() not in kill]

TH_ORDER=[
 ("Scales & Modes", TH["Scales & Modes"]),
 ("Chords",         CHORDS),
 ("Voicings",       VOICINGS),
 ("Rhythms",        dedup(strip(SONG["Rhythm & Time"]+TH["Rhythm & Meter"],CHORDS,VOICINGS))),
 ("Melody",         strip(SONG["Melody"],CHORDS,VOICINGS)),
 ("Harmony & Function", dedup(strip(TH["Harmony & Function"]+SONG["Harmony"],CHORDS,VOICINGS))),
 ("Counterpoint",   strip(TH["Counterpoint & Line"],CHORDS,VOICINGS)),
 ("Form",           dedup(strip(SONG["Form & Structure"]+TH["Form & Process"],CHORDS,VOICINGS))),
 ("Texture & Arrangement", strip(SONG["Texture & Arrangement"],CHORDS,VOICINGS)),
 ("Dynamics & Expression", SONG["Dynamics & Expression"]),
 ("Timbre & Tone",  SONG["Timbre & Tone"]),
 ("Lyrics & Voice", SONG["Lyrics & Voice"]),
 ("Tuning Systems", TH["Tuning & Systems"]),
]
P['theory']=("Theory","Reach for one you don't normally use. Constraint beats inspiration.",
             dict(TH_ORDER), None)

# ---- Adjectives: unchanged content, renamed deck ----
P['adjective']=("Adjectives","Say the sound before you name the plugin. Chase the word.",TEX,None)

# ---- Genres: unchanged ----
P['genre']=(gn,gb,GEN,None)

# ---- Abstract Nouns: single-word categories ----
P['abstract']=("Abstract Nouns","The thing the song is secretly about.",{
"Time":["Time","Duration","Moment","Eternity","Impermanence","Transience","Cycle","Repetition","Season","Anniversary","Youth","Age","Delay","Urgency","Patience","Beginning","Ending","Threshold","Now","Forever"],
"Change":["Change","Transformation","Becoming","Growth","Decay","Erosion","Renewal","Transition","Progress","Stagnation","Reversal","Departure","Return","Migration","Metamorphosis","Drift","Collapse","Emergence","Rupture","Adaptation"],
"Memory":["Memory","Forgetting","Recollection","Nostalgia","Amnesia","Trace","Residue","Echo","Imprint","Record","Witness","Testimony","History","Inheritance","Ancestry","Relic","Archive","Reminiscence","Hindsight","Erasure"],
"Knowledge":["Knowledge","Ignorance","Understanding","Insight","Intuition","Wisdom","Doubt","Certainty","Belief","Confusion","Clarity","Revelation","Curiosity","Learning","Mastery","Expertise","Naivety","Awareness","Perception","Judgment"],
"Desire":["Desire","Longing","Hunger","Thirst","Craving","Appetite","Lust","Ambition","Aspiration","Temptation","Obsession","Addiction","Yearning","Want","Need","Greed","Envy","Fixation","Indulgence","Restlessness"],
"Will":["Will","Resolve","Determination","Discipline","Drive","Motivation","Choice","Decision","Hesitation","Commitment","Sacrifice","Surrender","Refusal","Persistence","Restraint","Denial","Compromise","Defiance","Endurance","Intention"],
"Power":["Power","Authority","Control","Dominance","Submission","Hierarchy","Influence","Force","Command","Weakness","Strength","Leverage","Coercion","Conquest","Rule","Tyranny","Sovereignty","Empire","Rank","Status"],
"Order":["Order","Chaos","Structure","Anarchy","Law","Rule","System","Pattern","Discipline","Ritual","Custom","Convention","Tradition","Disorder","Entropy","Balance","Symmetry","Hierarchy","Method","Routine"],
"Freedom":["Freedom","Liberation","Autonomy","Independence","Bondage","Captivity","Constraint","Escape","Release","Exile","Wandering","Rootlessness","Choice","Openness","Boundlessness","Restriction","Confinement","Flight","Emancipation","Wildness"],
"Justice":["Justice","Injustice","Fairness","Judgment","Punishment","Mercy","Guilt","Innocence","Blame","Vengeance","Retribution","Forgiveness","Corruption","Integrity","Duty","Obligation","Rights","Wrong","Accountability","Verdict"],
"Connection":["Love","Friendship","Kinship","Community","Belonging","Solidarity","Loyalty","Trust","Intimacy","Companionship","Devotion","Bond","Reconciliation","Hospitality","Welcome","Recognition","Attachment","Care","Fellowship","Union"],
"Distance":["Distance","Estrangement","Separation","Absence","Alienation","Isolation","Loneliness","Exile","Displacement","Stranger","Border","Threshold","Silence","Withdrawal","Detachment","Indifference","Neglect","Abandonment","Departure","Gulf"],
"Truth":["Truth","Honesty","Authenticity","Confession","Disclosure","Transparency","Sincerity","Fact","Evidence","Proof","Reality","Accuracy","Candour","Frankness","Testimony","Admission","Revelation","Integrity","Openness","Verification"],
"Illusion":["Illusion","Lie","Deception","Mask","Facade","Pretense","Performance","Fantasy","Delusion","Hallucination","Mirage","Dream","Myth","Fiction","Disguise","Vanity","Glamour","Spectacle","Propaganda","Forgery"],
"Identity":["Identity","Self","Persona","Name","Anonymity","Reputation","Image","Role","Character","Ego","Shadow","Double","Reflection","Origin","Belonging","Difference","Otherness","Individuality","Conformity","Becoming"],
"Fate":["Fate","Destiny","Chance","Luck","Providence","Fortune","Coincidence","Inevitability","Prophecy","Omen","Curse","Blessing","Doom","Accident","Randomness","Design","Purpose","Predestination","Contingency","Odds"],
"Spirit":["Faith","Doubt","Grace","Sin","Redemption","Salvation","Damnation","Prayer","Ritual","Blessing","Transcendence","Sacredness","Reverence","Pilgrimage","Vision","Soul","Devotion","Worship","Mystery","Awe"],
"Loss":["Loss","Grief","Mourning","Death","Mortality","Absence","Void","Emptiness","Oblivion","Disappearance","Ruin","Wreckage","Wound","Scar","Trauma","Bereavement","Farewell","Extinction","Vanishing","Remains"],
"Survival":["Survival","Endurance","Resilience","Healing","Recovery","Repair","Persistence","Stubbornness","Hope","Refuge","Shelter","Sanctuary","Rescue","Salvage","Continuity","Toughness","Grit","Adaptation","Return","Rebirth"],
},None)

# ---- Production: finer categories ----
P['production']=("Production","What happens after the notes — the other half of the arrangement.",{
"Reverb":["Room","Hall","Chamber","Plate reverb","Spring reverb","Convolution reverb","Shimmer reverb","Gated reverb","Reverse reverb","Pre-delay","Decay time","Early reflections","Diffusion","Damping","Ambience","Bloom","Tail","Nonlinear reverb","Cathedral","Cave","Stairwell","Bathroom","Chamber echo","Ducked reverb","Sidechained reverb","Filtered reverb","Infinite reverb","Freeze verb","Blackhole","Dry/wet balance"],
"Delay":["Slapback","Tape delay","Analog delay","Digital delay","Ping-pong delay","Multi-tap delay","Dotted eighth delay","Triplet delay","Feedback","Modulated delay","Reverse delay","Granular delay","Dub delay","Filtered delay","Diffused delay","Ducked delay","Runaway feedback","Echo chamber","Oil-can delay","Bucket-brigade delay"],
"Modulation":["Chorus","Flanger","Phaser","Tremolo","Vibrato","Rotary speaker","Leslie","Ring modulation","Frequency shifter","Auto-pan","Univibe","Ensemble","Doubler","Detune","Unison spread","LFO","Envelope follower","Sample and hold","Wobble","Warble","Comb filter","Barber-pole flanging","Through-zero flanging","Harmonic tremolo","Chorusing","Random modulation","Cross modulation","Sync modulation","Pitch drift","Amplitude modulation"],
"Compression":["Compression","Limiting","Expansion","Gating","Attack time","Release time","Ratio","Threshold","Knee","Makeup gain","Sidechain","Ducking","Pumping","Breathing","Parallel compression","Bus compression","Multiband compression","Serial compression","Opto compression","FET compression","VCA compression","Vari-mu compression","Transient shaping","Upward compression","Downward expansion","Gate threshold","Hold time","Look-ahead","Peak limiting","RMS detection"],
"Distortion":["Saturation","Overdrive","Distortion","Fuzz","Bitcrushing","Sample-rate reduction","Clipping","Hard clipping","Soft clipping","Tape saturation","Tube warmth","Transformer colour","Harmonic exciter","Waveshaping","Foldback distortion","Octave fuzz","Amp breakup","Speaker breakup","Console drive","Preamp gain","Rectification","Asymmetric clipping","Even harmonics","Odd harmonics","Fizz","Crunch","Grit","Sizzle","Fry","Mangle"],
"EQ & Filtering":["EQ","High-pass filter","Low-pass filter","Band-pass filter","Notch filter","Shelf","Bell curve","Resonance","Cutoff","Q factor","Tilt EQ","Dynamic EQ","Linear-phase EQ","De-esser","Formant filter","Wah","Auto-wah","Envelope filter","Telephone filter","Vocal filter","Sub bass","Low-mid buildup","Mud","Boxiness","Harshness","Sibilance","Air band","Presence band","Notch sweep","Resonant sweep"],
"Stereo & Space":["Panning","Stereo width","Mid-side","Mono compatibility","Haas effect","Stereo spread","Binaural","Ambisonic","Surround","Immersive mix","Depth","Front-to-back","Center image","Phantom center","Phase","Polarity","Correlation","Comb filtering","Hard pan","Auto-pan sweep","Widening","Narrowing","Rotation","Collapse","Near field","Far field","Placement","Perspective","Proximity","Layer depth"],
"Pitch & Time":["Pitch shift","Formant shift","Harmonizer","Auto-tune","Pitch correction","Melodyne editing","Time stretch","Varispeed","Tape wow","Flutter","Doppler","Octave up","Octave down","Detune","Chipmunk effect","Slowed and reverbed","Half-speed","Double-speed","Reverse","Scrub"],
"Synthesis":["Subtractive synthesis","Additive synthesis","FM synthesis","Wavetable synthesis","Granular synthesis","Physical modelling","Vector synthesis","Phase distortion","Karplus-Strong","Oscillator","Sub oscillator","Noise generator","Filter envelope","Amplitude envelope","ADSR","Portamento","Glide","Unison","Voice stealing","Polyphony","Monophony","Ring mod oscillator","Hard sync","Pulse width modulation","Sample and hold source","Modulation matrix","Patch cable","Voltage control","Envelope depth","Key tracking"],
"Sampling":["Sampler","Slicing","Chopping","Time-stretching","Pitching a sample","Reversal","Layering","Round-robin","Velocity layers","Multisampling","Loop points","Crossfade loop","One-shot","Breakbeat chop","Vinyl sample","Field sample","Found sound","Foley sample","Vocal chop","Micro-sample"],
"Automation":["Automation","Fader ride","Filter sweep","Volume swell","Pan automation","Send automation","Mute automation","Parameter lock","Envelope drawing","Macro control","Modulation depth","Rise","Fall","Build","Drop","Riser","Downlifter","Impact","Transition effect","Gradual reveal"],
"Microphones":["Close-miking","Room miking","Spot mic","Overhead","Stereo pair","XY","ORTF","Blumlein","Mid-side miking","Decca tree","Ribbon mic","Condenser","Dynamic mic","Contact mic","Hydrophone","Boundary mic","Shotgun mic","Proximity effect","Off-axis colouration","Polar pattern"],
"Recording":["Multitrack","Overdub","Punch-in","Comping","Take","Live take","Bleed","Headphone mix","Click track","Scratch track","Direct injection","Re-amping","Amp simulation","Tape machine","Console","Preamp","Gain staging","Bouncing","Stem","Track sheet"],
"Mixing":["Balance","Level","Fader","Bus","Group","Aux send","Return","Insert","Sub-mix","Stem mix","Reference track","Translation","Headroom","Clip gain","Fader ride","Solo","Mute","Phase alignment","Frequency masking","Arrangement mixing"],
"Mastering":["Loudness","LUFS","True peak","Dynamic range","Limiting ceiling","Dithering","Sample rate conversion","Bit depth","Sequencing","Track spacing","Fade in","Fade out","Tonal balance","Mid-side mastering","Stem mastering","Reference matching","Codec check","Vinyl master","Streaming normalisation","Final polish"],
"Noise & Lo-Fi":["Tape hiss","Vinyl crackle","Surface noise","Hum","Buzz","Ground loop","Noise floor","Dropout","Wow and flutter","Azimuth error","Print-through","Cassette warble","Radio static","Bit reduction","Aliasing","Codec artefacts","Digital clipping","Glitch","Stutter","Degradation"],
},None)

# ---- strip multi-word compounds from the dictionary-backed word decks ----
def _single(seq): return [w for w in seq if " " not in w]
_n,_b,_g,_f = P['emotion']; P['emotion']=(_n,_b,_g,_single(_f))
for _k in ('adjective','abstract'):
    _n,_b,_g,_f = P[_k]
    P[_k]=(_n,_b,{c:_single(ws) for c,ws in _g.items()},_f)

# ---- Verbs ----
P['verb']=("Verbs","What the music does. Pick the action, then find the sound that performs it.",{
"Break":["Shatter","Crack","Split","Snap","Fracture","Rupture","Burst","Explode","Detonate","Implode","Collapse","Crumble","Crush","Smash","Demolish","Destroy","Wreck","Ruin","Raze","Shred","Tear","Rip","Rend","Sever","Cleave","Splinter","Fragment","Puncture","Pierce","Breach"],
"Build":["Build","Construct","Assemble","Erect","Forge","Fashion","Craft","Make","Create","Compose","Devise","Invent","Generate","Spawn","Breed","Cultivate","Grow","Nurture","Foster","Raise","Establish","Found","Lay","Stack","Layer","Weave","Knit","Braid","Sculpt","Mould"],
"Join":["Join","Merge","Fuse","Blend","Bind","Weld","Solder","Graft","Splice","Attach","Couple","Link","Chain","Bond","Unite","Combine","Mix","Mingle","Stir","Fold","Marry","Pair","Match","Align","Sync","Lock","Interlock","Nest","Embed","Integrate"],
"Divide":["Divide","Separate","Part","Halve","Slice","Carve","Cut","Chop","Sever","Isolate","Detach","Unhook","Unravel","Untangle","Disperse","Scatter","Strew","Sift","Sort","Filter","Strain","Extract","Distil","Refine","Peel","Strip","Shave","Pare","Prune","Thin"],
"Move":["Move","Travel","Drift","Float","Glide","Slide","Slip","Skid","Roll","Tumble","Spin","Whirl","Orbit","Circle","Wander","Roam","Stray","Meander","Weave","Zigzag","Dart","Dash","Sprint","Race","Hurtle","Careen","Lurch","Stagger","Stumble","Crawl"],
"Rise":["Rise","Ascend","Climb","Soar","Lift","Elevate","Hoist","Heave","Surge","Swell","Mount","Tower","Spike","Escalate","Bloom","Blossom","Unfold","Emerge","Surface","Dawn","Break","Erupt","Spring","Leap","Vault","Bound","Bounce","Rebound","Recoil","Spring back"],
"Fall":["Fall","Descend","Drop","Plunge","Plummet","Dive","Sink","Settle","Subside","Ebb","Recede","Wane","Fade","Dwindle","Diminish","Decay","Wither","Wilt","Droop","Sag","Slump","Slouch","Collapse","Cave","Crash","Tumble","Topple","Keel","Capsize","Founder"],
"Push":["Push","Shove","Thrust","Drive","Ram","Propel","Launch","Hurl","Fling","Toss","Cast","Eject","Expel","Repel","Force","Press","Squeeze","Compress","Cram","Wedge","Jam","Pin","Crowd","Herd","Corner","Trap","Corral","Confine","Restrict","Constrain"],
"Pull":["Pull","Drag","Haul","Tow","Tug","Yank","Wrench","Draw","Reel","Wind","Coil","Retract","Withdraw","Recall","Summon","Attract","Lure","Entice","Beckon","Invite","Gather","Collect","Amass","Hoard","Harvest","Reap","Glean","Scoop","Siphon","Absorb"],
"Open":["Open","Unfold","Unfurl","Spread","Splay","Expand","Widen","Broaden","Stretch","Extend","Dilate","Gape","Yawn","Part","Uncover","Unwrap","Unseal","Unlock","Release","Free","Loosen","Slacken","Relax","Ease","Vent","Air","Clear","Empty","Drain","Pour"],
"Close":["Close","Shut","Seal","Cap","Plug","Stop","Block","Bar","Dam","Choke","Stifle","Smother","Muffle","Mute","Damp","Contract","Narrow","Shrink","Tighten","Clench","Grip","Clamp","Clasp","Cradle","Enclose","Encircle","Surround","Envelop","Wrap","Swaddle"],
"Reveal":["Reveal","Expose","Unmask","Uncloak","Disclose","Betray","Confess","Admit","Announce","Declare","Proclaim","Broadcast","Publish","Display","Exhibit","Show","Present","Offer","Illuminate","Highlight","Underline","Emphasise","Clarify","Articulate","Define","Specify","Name","Label","Mark","Signal"],
"Hide":["Hide","Conceal","Cloak","Veil","Shroud","Mask","Disguise","Bury","Submerge","Sink","Obscure","Blur","Fog","Cloud","Shadow","Eclipse","Shade","Screen","Shield","Guard","Withhold","Suppress","Repress","Silence","Censor","Erase","Delete","Efface","Expunge","Forget"],
"Change":["Change","Alter","Modify","Adjust","Tune","Tweak","Shift","Swap","Trade","Substitute","Replace","Convert","Transform","Transmute","Morph","Mutate","Warp","Distort","Bend","Twist","Skew","Invert","Reverse","Flip","Rotate","Displace","Transpose","Translate","Adapt","Evolve"],
"Shape":["Shape","Form","Mould","Cast","Carve","Whittle","Chisel","Hammer","Beat","Pound","Flatten","Round","Smooth","Polish","Burnish","Sand","Roughen","Scar","Etch","Engrave","Inscribe","Stamp","Imprint","Emboss","Score","Notch","Groove","Ridge","Taper","Sharpen"],
"Strike":["Strike","Hit","Beat","Bash","Batter","Pummel","Thump","Knock","Rap","Tap","Pat","Slap","Smack","Whip","Lash","Flog","Kick","Stomp","Trample","Crush","Grind","Scrape","Scratch","Scuff","Graze","Brush","Stroke","Caress","Touch","Nudge"],
"Flow":["Flow","Stream","Run","Course","Rush","Gush","Spurt","Jet","Spray","Splash","Spill","Leak","Seep","Ooze","Trickle","Drip","Bleed","Weep","Pool","Puddle","Flood","Swamp","Drown","Immerse","Steep","Soak","Saturate","Wash","Rinse","Cleanse"],
"Burn":["Burn","Blaze","Flare","Flame","Scorch","Sear","Singe","Char","Smoulder","Smoke","Melt","Thaw","Boil","Simmer","Steam","Bake","Roast","Toast","Freeze","Chill","Cool","Ice","Frost","Crystallise","Harden","Set","Cure","Temper","Anneal","Quench"],
"Sound":["Sound","Ring","Chime","Toll","Peal","Clang","Clatter","Rattle","Hum","Buzz","Drone","Whine","Wail","Howl","Shriek","Scream","Roar","Bellow","Growl","Snarl","Hiss","Sigh","Whisper","Murmur","Mutter","Chant","Sing","Croon","Warble","Echo"],
"Sustain":["Sustain","Hold","Keep","Maintain","Preserve","Prolong","Extend","Linger","Dwell","Persist","Endure","Last","Remain","Stay","Wait","Pause","Rest","Suspend","Hover","Hang","Float","Idle","Loop","Repeat","Reiterate","Cycle","Recur","Return","Resume","Continue"],
"Pursue":["Chase","Pursue","Hunt","Stalk","Track","Trail","Follow","Shadow","Trace","Seek","Search","Hunt down","Flee","Escape","Evade","Dodge","Duck","Swerve","Veer","Elude","Outrun","Outpace","Overtake","Catch","Seize","Snatch","Grab","Clutch","Capture","Trap"],
"Give":["Give","Offer","Grant","Bestow","Award","Donate","Surrender","Yield","Concede","Relinquish","Abandon","Forsake","Discard","Dump","Shed","Spend","Waste","Squander","Lavish","Pour out","Take","Seize","Claim","Steal","Rob","Plunder","Devour","Consume","Drain","Deplete"],
},None)

# dedupe verbs across categories (first category wins) and drop multi-word entries
_n,_b,_g,_f = P['verb']
_seenv=set(); _vg={}
for _c,_ws in _g.items():
    _keep=[]
    for _w in _ws:
        if " " in _w: continue
        if _w.lower() in _seenv: continue
        _seenv.add(_w.lower()); _keep.append(_w)
    if _keep: _vg[_c]=_keep
P['verb']=(_n,_b,_vg,_f)

# ---- dedup pass: Abstract Nouns rebuilt so nothing repeats within it or against Emotions ----
import json as _json, os as _os
if _os.path.exists('abstract_clean.json'):
    _n,_b,_g,_f = P['abstract']
    P['abstract']=(_n,_b,_json.load(open('abstract_clean.json')),_f)

# ---- intra-deck dedup: a word appearing twice inside one deck is always a bug.
# (Cross-deck repeats are left alone — "Drop" means different things in Theory,
#  Production and Verbs, and each deck needs its own.)
for _k,( _n,_b,_g,_f) in list(P.items()):
    if _g is None: continue
    _seen=set(); _out={}
    for _c,_ws in _g.items():
        _keep=[]
        for _w in _ws:
            if _w.lower() in _seen: continue
            _seen.add(_w.lower()); _keep.append(_w)
        if _keep: _out[_c]=_keep
    P[_k]=(_n,_b,_out,_f)
