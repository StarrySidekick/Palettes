# -*- coding: utf-8 -*-
# Genuine affective states only. Nouns naming something a person can FEEL.
# Excluded on purpose: adjectives, character traits, physical sensations without
# affect, and abstract nouns that aren't felt states (justice, time, fate).
E = """
Joy Delight Glee Elation Euphoria Jubilation Exuberance Giddiness Cheer Cheerfulness
Buoyancy Playfulness Mirth Amusement Hilarity Merriment Levity Whimsy Sparkle Effervescence
Triumph Pride Satisfaction Contentment Gratification Fulfilment Gratitude Thankfulness
Appreciation Relief Reprieve Hope Hopefulness Optimism Anticipation Excitement Eagerness
Enthusiasm Zeal Zest Verve Ardour Fervour Rapture Bliss Ecstasy Serenity Ease Comfort
Warmth Affection Fondness Tenderness Endearment Adoration Devotion Reverence Admiration
Esteem Respect Veneration Worship Awe Wonder Amazement Astonishment Marvel Stupefaction
Bewilderment Fascination Curiosity Intrigue Enchantment Captivation Absorption Engrossment
Flow Immersion Presence Stillness Calm Peace Peacefulness Tranquility Repose Quietude
Restfulness Relaxation Equanimity Composure Poise Steadiness Assurance Confidence Security
Safety Trust Faith Conviction Certainty Clarity Illumination Epiphany Insight Realisation
Understanding Recognition Acceptance Resignation Surrender Humility Modesty Meekness
Sadness Sorrow Grief Mourning Bereavement Lamentation Woe Melancholy Melancholia Wistfulness
Pensiveness Rumination Brooding Nostalgia Homesickness Saudade Hiraeth Sehnsucht Longing
Yearning Pining Aching Hankering Wanderlust Regret Rue Remorse Contrition Penitence
Compunction Guilt Shame Mortification Humiliation Embarrassment Chagrin Abashment
Self-reproach Self-loathing Inadequacy Inferiority Worthlessness Disappointment Letdown
Disenchantment Disillusionment Dejection Despondency Downheartedness Discouragement
Demoralisation Gloom Dolour Anguish Torment Agony Heartache Heartbreak Devastation
Desolation Bleakness Hopelessness Despair Wretchedness Misery Distress Sorrowfulness
Emptiness Hollowness Numbness Deadness Anhedonia Apathy Listlessness Lethargy Languor
Ennui Boredom Tedium Weariness Fatigue Exhaustion Burnout Depletion Defeat Resignation
Loneliness Solitude Isolation Alienation Estrangement Abandonment Rejection Exclusion
Ostracism Forsakenness Orphanhood Anger Rage Fury Wrath Ire Choler Indignation Outrage
Umbrage Offence Affront Resentment Rancour Bitterness Acrimony Spite Malice Vindictiveness
Vengefulness Hatred Loathing Abhorrence Detestation Animosity Enmity Hostility Antagonism
Aggression Belligerence Pugnacity Irritation Annoyance Vexation Exasperation Aggravation
Displeasure Discontent Grievance Frustration Thwartedness Impatience Restlessness Agitation
Fretfulness Petulance Peevishness Crankiness Irascibility Contempt Scorn Disdain Derision
Condescension Sneering Disgust Revulsion Repugnance Distaste Aversion Nausea Squeamishness
Horror Repulsion Defiance Rebelliousness Insubordination Obstinacy Stubbornness
Righteousness Indignance Jealousy Envy Covetousness Possessiveness Betrayal Fear Terror
Dread Panic Alarm Fright Startlement Horror Trepidation Apprehension Foreboding Misgiving
Anxiety Angst Worry Concern Unease Disquiet Nervousness Jitteriness Edginess Tension
Strain Pressure Stress Overwhelm Dismay Consternation Perturbation Paranoia Suspicion
Distrust Mistrust Wariness Caution Timidity Shyness Bashfulness Diffidence Insecurity
Self-doubt Uncertainty Doubt Hesitance Indecision Ambivalence Vulnerability Exposure
Defencelessness Helplessness Powerlessness Impotence Hopelessness Entrapment Claustrophobia
Vertigo Disorientation Dizziness Confusion Perplexity Puzzlement Befuddlement Doubtfulness
Love Amorousness Infatuation Limerence Passion Lust Desire Craving Hunger Thirst Appetite
Attraction Chemistry Yearning Flirtatiousness Coquetry Romance Intimacy Closeness Bonding
Attachment Kinship Camaraderie Fellowship Companionship Solidarity Belonging Loyalty
Fidelity Allegiance Compassion Empathy Sympathy Pity Commiseration Tenderheartedness
Kindliness Benevolence Goodwill Charity Altruism Care Concern Protectiveness Nurturance
Maternal-feeling Paternal-feeling Forgiveness Absolution Reconciliation Mercy Clemency
Generosity Magnanimity Openness Receptivity Vulnerability Candour Sincerity Earnestness
Transcendence Sublimity Numinousness Sacredness Solemnity Piety Devoutness Grace Blessedness
Redemption Salvation Consolation Solace Catharsis Release Unburdening Lightness Weightlessness
Buoyance Elevation Uplift Inspiration Muse Creativity Ingenuity Flowstate Determination
Resolve Grit Tenacity Perseverance Fortitude Courage Bravery Valour Boldness Audacity
Daring Recklessness Abandon Wildness Ferocity Intensity Vehemence Passionateness Drive
Ambition Aspiration Hunger-for-more Competitiveness Rivalry Bittersweetness Poignancy
Melancholic-joy Wistful-longing Sweet-sorrow Tender-grief Angry-love Reluctant-affection
Fond-exasperation Guilty-pleasure Schadenfreude Gloating Smugness Self-satisfaction
Complacency Vanity Conceit Arrogance Hubris Haughtiness Pomposity Superiority Entitlement
Indifference Detachment Dissociation Depersonalisation Derealisation Unreality Uncanniness
Eeriness Creepiness Dread-anticipation Suspense Cliffhanging Impatient-hope Nervous-excitement
Anxious-joy Fearful-awe Reverent-terror Holy-dread Sublime-terror Cynicism Jadedness
World-weariness Disaffection Nihilism Absurdity Irony Sardonicism Bemusement Wryness
Dark-humour Gallows-humour Mischief Impishness Naughtiness Devilment Glee-in-mischief
Anticipatory-delight Vicarious-joy Compersion Sympathetic-joy Pride-in-another
Protective-rage Righteous-anger Moral-outrage Disgust-at-injustice Grief-for-a-stranger
Collective-grief Collective-joy Effervescent-togetherness Communion Rapport Attunement
Resonance Recognition-of-another Being-seen Being-known Being-held Feeling-safe
Feeling-wanted Feeling-chosen Feeling-forgotten Feeling-replaceable Feeling-invisible
Feeling-trapped Feeling-free Feeling-alive Aliveness Vitality Vigour Animation Sprightliness
Sluggishness Heaviness Torpor Drowsiness Somnolence Dreaminess Reverie Daydreaming
Absentmindedness Distraction Preoccupation Obsession Fixation Compulsion Craving-loop
Withdrawal Cravenness Cowardice Shamelessness Brazenness Impudence Insolence Cheek
Sauciness Flippancy Nonchalance Blitheness Carelessness Heedlessness Recklessness-of-heart
Tenderness-toward-self Self-compassion Self-forgiveness Self-acceptance Self-respect
Self-consciousness Self-criticism Perfectionism Scrupulosity Obligation Duty-feeling
Indebtedness Beholdenness Gratefulness Obligation-fatigue Resentful-duty Martyrdom
Longing-for-home Longing-for-the-past Longing-for-a-stranger Longing-for-what-never-was
Anticipated-loss Pre-emptive-grief Survivor-guilt Relief-tinged-with-guilt
Hope-against-hope Stubborn-hope Fragile-hope Quiet-joy Fierce-joy Defiant-joy
Sorrowful-gratitude Grateful-grief Peaceful-sadness Content-loneliness Comfortable-silence
Awkwardness Cringe Secondhand-embarrassment Vicarious-shame Social-dread Stage-fright
Performance-anxiety Impostor-feeling Exposure-anxiety Scrutiny Being-watched Paranoid-unease
Homely-warmth Coziness Snugness Nestledness Sanctuary-feeling Shelteredness Refuge-feeling
Belonging-to-a-place Rootedness Groundedness Centredness Wholeness Integration Alignment
Fragmentation Brokenness Shatteredness Unravelling Disintegration Overwhelm-flood
Emotional-flooding Sensory-overload Shutdown Freeze Fawning Startle-response Hypervigilance
Dread-of-the-phone Sunday-dread Morning-dread Nameless-sadness Formless-anxiety
Free-floating-dread Existential-anxiety Death-anxiety Cosmic-loneliness Insignificance
Smallness Vastness-awe Oceanic-feeling Unity-feeling Dissolution-of-self Ego-death
Mystical-joy Beatitude Rapturous-surrender Devotional-longing Sacred-yearning
Spiritual-dryness Dark-night-feeling Abandonment-by-God Doubt-of-faith Renewed-faith
Conversion-feeling Repentance Absolution-relief Vindication Exoneration Acquittal-relief
Reprieve-joy Homecoming-joy Reunion-joy Recognition-joy Discovery-thrill Eureka-feeling
Breakthrough Momentum Being-on-a-roll Winning-feeling Losing-feeling Near-miss-agony
Almost-had-it Sour-grapes Bitter-acceptance Grudging-respect Reluctant-admiration
Fond-contempt Affectionate-mockery Teasing-warmth Sibling-rivalry Protective-jealousy
Romantic-jealousy Professional-envy Aesthetic-envy Admiring-envy Benign-envy Malicious-envy
Longing-for-recognition Craving-approval Fear-of-abandonment Fear-of-engulfment
Fear-of-intimacy Fear-of-failure Fear-of-success Fear-of-being-known Relief-at-being-known
Tenderness-at-vulnerability Awe-at-another Heartswell Heart-fullness Chest-tightness-of-love
Lump-in-throat Welling Tearfulness Weepiness Sobbing-release Laughter-through-tears
Hysteria Giddy-relief Nervous-laughter Manic-elation Hypomania Restless-euphoria
Crash Comedown Post-elation-flatness Anticlimax Deflation Letdown-after-triumph
Emptiness-after-completion Purposelessness Aimlessness Driftlessness Rudderlessness
Stuckness Stagnation-feeling Claustrophobic-boredom Itch-for-change Wanderlust-restlessness
Itchy-feet Springtime-restlessness Autumnal-melancholy Winter-heaviness Summer-languor
Twilight-sadness Dawn-hope Insomniac-dread Three-am-clarity Three-am-terror
"""
WORDS=[w.strip() for w in E.split() if w.strip()]
