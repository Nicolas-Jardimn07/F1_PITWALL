# ─────────────────────────────────────────────────────────────────────────────
#  STATIC CONTENT — engineering, glossary, radio phrases, interview vocab
# ─────────────────────────────────────────────────────────────────────────────

ENGINEERING_SECTIONS = {
    "🔧 Aerodynamics": [
        (
            "Downforce & Drag Balance", "#e10600",
            "Every aerodynamic surface generates a trade-off: more downforce = more grip in corners, "
            "but also more drag on straights. Teams constantly adjust wing angles (rake) between circuits "
            "depending on whether the track prioritises cornering or straight-line speed.",
        ),
        (
            "DRS — Drag Reduction System", "#e10600",
            "The rear wing features a movable flap that opens when the driver activates DRS, reducing drag by ~10% "
            "and adding 10–15 km/h on the straight. Only usable within 1 second of the car ahead in designated zones.",
        ),
        (
            "Ground Effect & Floor", "#e10600",
            "Since 2022, F1 cars generate the majority of their downforce from the underfloor (Venturi tunnels) "
            "rather than wings. Air accelerates under the car, creating a low-pressure zone that sucks the car to the track.",
        ),
        (
            "Rake Angle", "#e10600",
            "The angle between the front and rear of the car floor. Higher rake = more downforce from the diffuser "
            "but less efficient. Teams choose based on circuit characteristics.",
        ),
    ],
    "⚙️ Power Unit": [
        (
            "Hybrid System (PU Architecture)", "#3671C6",
            "The 2022–2025 PU consists of: ICE (Internal Combustion Engine, 1.6L V6 turbo), "
            "MGU-K (Motor Generator Unit–Kinetic, up to 120 kW), MGU-H (Motor Generator Unit–Heat, "
            "recovering energy from exhaust gases). From 2026, the MGU-H is removed, and electrical "
            "output increases significantly.",
        ),
        (
            "ERS — Energy Recovery System", "#3671C6",
            "The MGU-K harvests kinetic energy under braking and deploys it as electric power on acceleration. "
            "Drivers get ~33 seconds of full ERS deployment per lap (4 MJ limit). Managing the battery state-of-charge "
            "is a critical strategic call during races.",
        ),
        (
            "Power Mode vs Reliability Mode", "#3671C6",
            "Teams run different engine maps depending on race situation. 'Quali mode' maximises power output "
            "at the cost of component life. 'Harvest mode' prioritises energy recovery. Engineers call these "
            "changes over radio using code phrases.",
        ),
        (
            "Turbocharger & MGU-H", "#3671C6",
            "The turbocharger spins a compressor to force more air into the engine. The MGU-H sits on the turbo shaft, "
            "both controlling turbo lag and harvesting excess energy. Removing it in 2026 rules will require new "
            "solutions for turbo lag management.",
        ),
    ],
    "🏎️ Chassis & Suspension": [
        (
            "Pull-rod vs Push-rod Suspension", "#FF8000",
            "The orientation of the suspension rocker arm affects weight distribution and airflow. "
            "Pull-rod (rear) is preferred by most teams for aero efficiency; push-rod (front) "
            "keeps weight higher, benefiting downforce generation under the nose.",
        ),
        (
            "Tyre Management & Thermal Window", "#FF8000",
            "Each tyre compound has a thermal window (operating temperature range) of ~20-30°C width. "
            "Too cold = no grip; too hot = graining or blistering. Engineers monitor tyre temperatures "
            "via infrared sensors and manage them through driving style instructions.",
        ),
        (
            "Differential", "#FF8000",
            "The rear differential controls power split between the two rear wheels. A more locked diff "
            "improves traction on corner exit but increases understeer on entry. Teams adjust diff maps "
            "electronically for each corner type.",
        ),
        (
            "Ballast & Weight Distribution", "#FF8000",
            "F1 cars must meet a minimum weight of 798 kg. Teams use ballast (usually tungsten or lead) "
            "to hit this target while placing the weight optimally — usually as low as possible "
            "to lower the centre of gravity and improve handling.",
        ),
    ],
    "📊 Strategy & Simulation": [
        (
            "Undercut & Overcut", "#27F4D2",
            "Undercut: pit before your rival to gain track position on fresher tyres. "
            "Overcut: stay out longer and benefit from lighter fuel load / rivals caught in traffic. "
            "The decision is calculated in real-time by strategy software on the pit wall.",
        ),
        (
            "Tyre Stint Modelling", "#27F4D2",
            "Engineers build lap-time models that degrade as a function of tyre age, fuel load, "
            "track temperature, and compound. Crossing these models with rival data allows them to "
            "predict the optimal pit window with 1–2 lap accuracy.",
        ),
        (
            "Fuel Load Strategy", "#27F4D2",
            "Cars start with exactly the amount of fuel needed to finish plus a small reserve. "
            "Each kg of fuel = ~0.035 seconds per lap. Saving fuel by lifting and coasting (L&C) "
            "is a constant instruction during races — visible as throttle spikes on the telemetry.",
        ),
        (
            "Safety Car Deployment Impact", "#27F4D2",
            "A Safety Car bunches the field and closes gaps, effectively neutralising a lead. "
            "Teams use this window to pit without losing position — if they read the timing correctly. "
            "A poorly timed SC pit can cost 20+ seconds and multiple positions.",
        ),
    ],
}

GLOSSARY = [
    ("Understeer",            "Subviragem",
     "Car doesn't turn enough — front washes wide. Speed loss at corner entry, can't hit the apex."),
    ("Oversteer",             "Sobreviragem",
     "Rear steps out — more rotation than steering commands. Driver must counter-steer."),
    ("Trail Braking",         "Frenagem progressiva",
     "Light brake pressure maintained while turning in. Loads front tyres, delays rotation point."),
    ("Apex / Clipping Point", "Ápice da curva",
     "Innermost corner point where car clips the kerb. Late apex = better exit speed."),
    ("Tyre Degradation",      "Degradação de pneu",
     "Progressive grip loss over a stint. Shows as rising lap times from heat cycling and wear."),
    ("Graining",              "Granulação",
     "Rubber chunks torn from tyre surface and re-deposited. Kills grip until grains clear."),
    ("Blistering",            "Bolhamento",
     "Heat blisters under tyre surface from excessive temps. Can cause sudden failure."),
    ("ERS Deployment",        "Acionamento do MGU-K",
     "Motor Generator Unit releases up to 120 kW on straights. Visible as speed spike on trace."),
    ("DRS",                   "Sistema de redução de arrasto",
     "Rear wing opens on straights within 1s of car ahead. Adds ~15 km/h."),
    ("Delta Time",            "Diferença de tempo",
     "Cumulative gap between two drivers. Gold line above zero = driver A losing time."),
    ("Snap",                  "Rotação brusca da traseira",
     "Sudden rear breakaway — abrupt throttle lift visible on trace. Can cause spin."),
    ("Locking Up",            "Travamento de roda",
     "Brake exceeds tyre grip — wheel stops while car moves. Creates flat spot."),
    ("Full Throttle Zone",    "Zona de aceleração máxima",
     "Straights where driver holds 100%. Longer zones = faster circuit overall."),
    ("Braking Point",         "Ponto de frenagem",
     "Marker where braking begins. Later = more aggressive / higher risk."),
    ("Out-lap / In-lap",      "Volta de saída / entrada",
     "Out-lap: warming tyres after pit. In-lap: managing everything before pitting."),
    ("Stint",                 "Stint",
     "Period on track between tyre changes. Length determines race strategy."),
    ("Marbles",               "Borracha solta fora da linha",
     "Rubber debris off racing line. Stepping on them = sudden massive grip loss."),
    ("Downforce",             "Carga aerodinâmica",
     "Aero force pushing car into tarmac. More grip in corners, more drag on straights."),
    ("Box Box Box",           "Pit stop",
     "Radio call to pit. Repeated 3× to cut through engine noise."),
    ("Purple/Green/Yellow",   "Setor roxo / verde / amarelo",
     "Purple=session fastest; Green=personal best; Yellow=slower than personal best."),
    ("Thermal Window",        "Janela térmica",
     "Temperature range where compound delivers optimal grip. Outside it = severe loss."),
    ("Undercut / Overcut",    "Estratégia de pit stop",
     "Undercut: pit early for track position on fresh tyres. Overcut: stay out, gain from traffic."),
]

# (phrase_en, context, portuguese_meaning, who_says)
RADIO_PHRASES = [
    ("Box, box, box",
     "Repeated 3× to cut through engine noise. The engineer calls the driver in for a pit stop.",
     "Entre nos boxes agora — pit stop", "Engineer → Driver"),
    ("Copy that",
     "Driver acknowledges an instruction. Used instead of 'OK' or 'understood'.",
     "Entendido / Certo", "Driver → Engineer"),
    ("We are in trouble with the tyres",
     "Driver warning about tyre performance. Usually means graining, blistering or high deg.",
     "Estamos com problema nos pneus", "Driver → Engineer"),
    ("Push, push, push",
     "Engineer tells driver to push flat-out — usually after a safety car or in qualifying.",
     "Acelera, vai fundo agora", "Engineer → Driver"),
    ("Tyre temperature is not in the window",
     "Tyres are too cold or too hot to perform. Common after SC restart or out-lap.",
     "O pneu não está na temperatura ideal", "Engineer → Driver"),
    ("Delta is plus two",
     "Driver is 2 seconds behind the target pace. 'Delta' = gap to required time.",
     "Você está 2 segundos abaixo do ritmo alvo", "Engineer → Driver"),
    ("Save fuel, lift and coast",
     "Driver must save fuel by lifting off throttle before braking points.",
     "Economize combustível, levante o pé antes de frear", "Engineer → Driver"),
    ("DRS is available",
     "Driver can now activate the rear wing flap to reduce drag on the straight.",
     "DRS liberado — pode abrir a asa", "Engineer → Driver"),
    ("Gap to car ahead is 1.2",
     "Time gap to the car in front — relevant for DRS activation (<1.0s).",
     "Diferença para o carro à frente é 1,2 segundos", "Engineer → Driver"),
    ("We need to manage the front left",
     "Specific tyre corner has degradation. Driver must adjust driving style.",
     "Precisamos cuidar do pneu dianteiro esquerdo", "Engineer → Driver"),
    ("Safety car is in this lap",
     "Safety car will enter pit lane at end of this lap — green flag racing next lap.",
     "O safety car entra nos boxes nessa volta — pista liberada", "Race Control broadcast"),
    ("Virtual Safety Car deployed",
     "VSC: all drivers must hold minimum lap delta. No overtaking.",
     "Virtual Safety Car ativado — todos seguram o delta", "Race Control broadcast"),
    ("Understood, fighting for position",
     "Driver acknowledges they're in a battle and can race hard.",
     "Entendido, estou brigando por posição", "Driver → Engineer"),
    ("We have an issue with the engine",
     "Mechanical problem. Engineer may ask driver to change engine mode.",
     "Temos um problema com o motor", "Driver → Engineer"),
    ("Compound is going off",
     "Tyre performance dropping rapidly — graining or past thermal window.",
     "O pneu está perdendo aderência rapidamente", "Driver → Engineer"),
    ("Multi-21 / team orders",
     "Code phrase for team orders — 'hold position behind teammate'.",
     "Ordem de equipe — mantenha posição", "Engineer → Driver"),
    ("Brilliant job, mate. Well done",
     "Post-race congratulation over radio. Common from both engineers and drivers.",
     "Trabalho excelente, muito bem feito", "Engineer → Driver"),
    ("What's the plan for the safety car?",
     "Driver asking strategy — should I pit or stay out under SC?",
     "Qual é o plano com o safety car? Paro ou fico?", "Driver → Engineer"),
    ("Gap to car behind is 4 seconds",
     "Engineer giving rear gap information — often to avoid pitting into traffic.",
     "Diferença para o carro de trás é 4 segundos", "Engineer → Driver"),
    ("We are P3 on the road",
     "Current track position — 'P' = position. 'On the road' = before virtual results.",
     "Estamos em 3º lugar na pista neste momento", "Engineer → Driver"),
    ("Front wing is damaged",
     "Driver reports aero damage — engineer checks cameras and advises on safety.",
     "A asa dianteira está danificada", "Driver → Engineer"),
    ("Watch your mirrors, car behind is close",
     "Engineer warning of a faster car approaching — defend or let past.",
     "Olha no espelho, tem um carro atrás chegando perto", "Engineer → Driver"),
    ("Hunting mode",
     "Push flat-out to close on the car ahead — tyres and engine at maximum.",
     "Modo caçada — vai fundo atrás do carro à frente", "Engineer → Driver"),
    ("You are free to race",
     "Cancellation of team orders — driver can race on their own terms.",
     "Você está livre para correr", "Engineer → Driver"),
    ("Tyre pressure is dropping",
     "Warning of possible slow puncture — driver may need to pit urgently.",
     "A pressão do pneu está caindo", "Engineer → Driver"),
    ("ERS is full, deploy when ready",
     "Battery fully charged — driver can use maximum electric power.",
     "ERS está cheio, aciona quando quiser", "Engineer → Driver"),
    ("Bring it home",
     "Car has an issue — save it, no risks, get back to the pits safely.",
     "Traga o carro de volta — sem riscos", "Engineer → Driver"),
    ("Red flag, red flag, red flag",
     "Session stopped — slow down and return to pit lane immediately.",
     "Bandeira vermelha — sessão parada, volte aos boxes", "Race Control broadcast"),
    ("Fastest lap is available",
     "Driver can attack for the bonus championship point — 1 pt for FL.",
     "A volta mais rápida está disponível — ponto extra em jogo", "Engineer → Driver"),
    ("Oil pressure is low",
     "Serious mechanical warning — driver may need to retire the car.",
     "Pressão de óleo está baixa — problema mecânico sério", "Engineer → Driver"),
]

# (phrase_en, context, portuguese_meaning)
INTERVIEW_PHRASES = [
    ("To be honest with you / If I'm being honest",
     "Filler phrase before giving a direct answer. Every F1 driver uses this constantly.",
     "Sendo honesto / Para ser honesto com você"),
    ("We need to go through the data",
     "Standard answer after any issue — engineers will analyse telemetry and find causes.",
     "Precisamos analisar os dados / Ver a telemetria"),
    ("The pace was there",
     "The car had the speed to compete, but something else went wrong (strategy, tyres, luck).",
     "O ritmo estava lá / Tínhamos velocidade"),
    ("It was a difficult weekend",
     "Diplomatic way to say the team had problems without blaming specific people.",
     "Foi um fim de semana difícil"),
    ("We put it all together",
     "Everything worked perfectly — car, strategy, driver, team all clicked.",
     "Colocamos tudo junto / Tudo encaixou"),
    ("I gave it everything I had",
     "Driver pushed to the absolute maximum — nothing held back.",
     "Dei tudo o que tinha / Me esforcei ao máximo"),
    ("The tyres came alive after a few laps",
     "Tyres reached operating temperature and started gripping properly.",
     "Os pneus começaram a funcionar depois de algumas voltas"),
    ("Massive thanks to the whole team",
     "Standard podium speech opener — always thanking the hundreds of factory staff.",
     "Enorme obrigado a toda a equipe"),
    ("We'll come back stronger",
     "After a bad result — optimistic statement about future performance.",
     "Voltaremos mais fortes"),
    ("It's a long season",
     "Used to downplay a bad result — many races still to go, season not over.",
     "É uma temporada longa"),
    ("I was on a different strategy",
     "Explaining why your lap times were different — saving tyres or fuel for later.",
     "Eu estava em uma estratégia diferente"),
    ("The car felt amazing today",
     "Car was perfectly set up — balance, downforce, tyres all working.",
     "O carro estava incrível hoje"),
    ("We maximised our points today",
     "Got everything possible from the weekend given the car's actual pace.",
     "Maximizamos nossos pontos hoje"),
    ("The balance was tricky today",
     "Car setup was unstable — too much oversteer or understeer in certain conditions.",
     "O balanço do carro estava complicado hoje"),
    ("We fell into the undercut",
     "Rival pitted earlier and came out ahead on fresher tyres — strategy miscalculation.",
     "Caímos no undercut — o rival saiu na frente com pneu novo"),
    ("We'll review and come back stronger",
     "Post-DNF or bad result standard answer — analysis first, then bounce back.",
     "Vamos revisar e voltar mais fortes"),
    ("The safety car really changed the race for us",
     "SC either helped (bunched field, free pit) or hurt (lost a gap).",
     "O safety car realmente mudou a corrida para nós"),
    ("We executed the strategy perfectly",
     "The pit stop timing, tyre choice and driver pace all came together.",
     "Executamos a estratégia perfeitamente"),
]

# (term, definition, portuguese)
BROADCAST_VOCAB = [
    ("On the limit",        "Driving at the absolute edge of grip/control",                        "No limite"),
    ("Flat out",            "100% throttle, no lifting",                                            "A fundo / Acelerador no chão"),
    ("The gap is closing",  "The driver behind is getting closer",                                  "A diferença está diminuindo"),
    ("Into the points",     "Driver has entered the top 10 (scoring positions)",                    "Nos pontos / No top 10"),
    ("Off the pace",        "Significantly slower than expected",                                   "Fora do ritmo"),
    ("Flying lap",          "Qualifying hot lap — maximum attack, fresh tyres",                     "Volta lançada / Volta classificatória"),
    ("Undercut worked",     "Pitstop strategy was faster than staying out",                         "O undercut funcionou"),
    ("Locked up",           "Wheels stopped under braking, skid marks on track",                   "Rodas travadas na frenagem"),
    ("Snap of oversteer",   "Sudden rear slide — driver catches it or spins",                       "Sobreviragem brusca"),
    ("On the radio",        "Driver is communicating with engineer right now",                      "No rádio / Falando com o engenheiro"),
    ("Pit window is open",  "Strategic moment when pitting won't lose track position",              "Janela de pit aberta"),
    ("Race pace",           "Sustained speed over many laps (vs qualifying one-lap pace)",          "Ritmo de corrida"),
    ("Yellow sector",       "Driver's sector time was slower than personal best",                   "Setor amarelo / Pior que o melhor pessoal"),
    ("Personal best",       "Driver's fastest sector time of the session so far",                  "Melhor tempo pessoal"),
    ("Championship leader", "Driver currently leading the drivers' standings",                      "Líder do campeonato"),
    ("DNF",                 "Did Not Finish — retired from the race",                              "Não completou a corrida"),
    ("Safety car window",   "Lap window where pitting under SC doesn't lose position",             "Janela do safety car"),
    ("Track position",      "Physical position on track vs competitors after pit stops",            "Posição na pista"),
    ("On the podium",       "Finishing P1, P2 or P3 — the top three positions",                   "No pódio — top 3"),
    ("VSC",                 "Virtual Safety Car — all drivers hold a minimum delta time",          "VSC — velocidade controlada"),
    ("Formation lap",       "Warm-up lap before the race start — drivers heat tyres and brakes",   "Volta de formação"),
    ("Chequered flag",      "Race is finished — the flag shown at the finish line",                "Bandeira quadriculada — fim da corrida"),
    ("Parc fermé",          "After qualifying, cars sealed — no setup changes allowed",            "Parque fechado — mudanças no carro proibidas"),
    ("Wheel-to-wheel",      "Drivers side-by-side fighting for position",                          "Roda a roda — disputa lado a lado"),
    ("Tyre deg",            "Short for tyre degradation — how fast the tyre loses performance",    "Degradação do pneu"),
]

PODIUM_INTERVIEW_SCRIPT = """**Typical Podium Interview — P1 Winner**

**Interviewer:** "How does it feel to win today?"
**Driver:** "It feels *incredible*. I have to give a massive thanks to the whole team — they gave me a great car today. We just had to manage the race, manage the tyres, and bring it home."

**Interviewer:** "Was there any point where you felt the lead was under threat?"
**Driver:** "Honestly, yes, I could feel the *gap was closing* in the second stint. My engineer told me to push and I was able to respond. We had the *pace* when we needed it."

**Interviewer:** "The championship picture — what does this mean?"
**Driver:** "Look, it's a *long season*. Every point counts. We'll go through the *data*, understand what worked, and come back to the next race even stronger."

---

**Typical Podium Interview — P3 Driver**

**Interviewer:** "P3 — are you happy with the result?"
**Driver:** "I mean, *to be honest*, I think we *maximised our points* today given where we were. The *race pace* wasn't quite there but the strategy call was good and we made it work."

**Interviewer:** "The early safety car changed the race?"
**Driver:** "Completely. We were on a *different strategy* and when the *safety car window* opened we had to make a quick call. It *paid off*. Credit to the *whole team*."

---

**Post-Qualifying — Pole Position Interview**

**Interviewer:** "Pole position — what was the key to that lap?"
**Driver:** "The car was *on the limit* the whole lap. I had to *nail every apex* — especially in the *final sector*. The team gave me a *fantastic* car this weekend."

**Interviewer:** "Any concerns for the race tomorrow?"
**Driver:** "We're *in parc fermé* now so no setup changes. I think our *race pace* is strong. *Tyre deg* here is always a factor. We've done the simulations and *we have a plan*."

---

**Post-Race — After a DNF**

**Interviewer:** "What happened out there?"
**Driver:** "We had a *mechanical issue* — I felt something wasn't right in sector 2. It's *gutting* obviously. We had the pace to *fight for the podium* today."

**Interviewer:** "How do you regroup from this?"
**Driver:** "You *move on*. There are still *many races left*. We'll *go through the data*, understand the issue, and *come back stronger* at the next race."

---

**Press Conference — Championship Contender**

**Journalist:** "You're now 15 points behind. Do you believe you can still win it?"
**Driver:** "Absolutely. *Fifteen points is nothing* in this sport. We just need to *execute perfectly*, score *maximum points* and let *the racing decide*."

**Journalist:** "How much pressure do you feel?"
**Driver:** "I *thrive on pressure*. The whole team is *united*, we have a *clear plan*, and we believe in *ourselves*. That's all you can do."
"""
