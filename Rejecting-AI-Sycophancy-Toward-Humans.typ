#show terms.item: it => block(breakable: false)[
  #text(weight: "bold")[#it.term]
  #block(inset: (left: 1.5em, top: -0.4em))[#it.description]
]

#set table(
  inset: 6pt,
  stroke: rgb("#d5dde7")
)

#show heading.where(level: 1): set text(font: ("Libertinus Serif", "New York", "Times New Roman"), size: 17pt, weight: "semibold")
#show heading.where(level: 2): set text(font: ("Libertinus Serif", "New York", "Times New Roman"), size: 13pt, weight: "semibold")
#show heading.where(level: 3): set text(font: ("Libertinus Serif", "New York", "Times New Roman"), size: 11pt, weight: "semibold")
#show heading: set block(above: 1.2em, below: 0.6em)

#show figure.where(
  kind: table
): set figure.caption(position: top)

#show figure.where(
  kind: image
): set figure.caption(position: bottom)

#let content-to-string(content) = {
  if content.has("text") {
    content.text
  } else if content.has("children") {
    content.children.map(content-to-string).join("")
  } else if content.has("body") {
    content-to-string(content.body)
  } else if content == [ ] {
    " "
  }
}
#let conf(
  title: none,
  subtitle: none,
  authors: (),
  keywords: (),
  date: none,
  abstract-title: none,
  abstract: none,
  thanks: none,
  cols: 1,
  margin: (x: 1.25in, y: 1.25in),
  paper: "us-letter",
  lang: "en",
  region: "US",
  font: none,
  fontsize: 11pt,
  mathfont: none,
  codefont: none,
  linestretch: 1,
  sectionnumbering: none,
  linkcolor: none,
  citecolor: none,
  filecolor: none,
  pagenumbering: "1",
  doc,
) = {
  set document(
    title: title,
    keywords: keywords,
  )
  set document(
      author: authors.map(author => content-to-string(author.name)).join(", ", last: " & "),
  ) if authors != none and authors != ()
  set page(
    paper: paper,
    margin: margin,
    numbering: pagenumbering,
    columns: cols
  )

  set par(
    justify: true,
    leading: linestretch * 0.65em
  )
  set text(lang: lang,
           region: region,
           size: fontsize)

  set text(font: font) if font != none
  show math.equation: set text(font: mathfont) if mathfont != none
  if codefont != none {
    show raw.where(block: false): it => box(
      fill: rgb("#f1f5f9"),
      inset: (x: 2.2pt, y: 0.8pt),
      radius: 2pt,
    )[
      #text(font: ("Libertinus Serif", "New York", "Times New Roman"), size: 0.92em, fill: rgb("#334155"))[#it]
    ]
    show raw.where(block: true): it => block(
      width: 100%,
      inset: 9pt,
      fill: rgb("#f8fafc"),
      stroke: 0.6pt + rgb("#dbe4ef"),
      radius: 3pt,
      breakable: true,
    )[
      #set text(font: ("Libertinus Serif", "New York", "Times New Roman"), size: 9.6pt, fill: rgb("#1f2937"))
      #set par(justify: false, leading: 0.58em)
      #it
    ]
  }

  set heading(numbering: sectionnumbering)

  show link: set text(fill: rgb(content-to-string(linkcolor))) if linkcolor != none
  show ref: set text(fill: rgb(content-to-string(citecolor))) if citecolor != none
  show link: this => {
    if filecolor != none and type(this.dest) == label {
      text(this, fill: rgb(content-to-string(filecolor)))
    } else {
      text(this)
    }
  }

  if title != none {
    place(top, float: true, scope: "parent", clearance: 4mm, block(below: 1em, width: 100%)[
      #if title != none {
        align(center, block[
            #text(font: ("Libertinus Serif", "New York", "Times New Roman"), weight: "semibold", size: 1.5em, hyphenate: false)[#title #if thanks != none {
                footnote(thanks, numbering: "*")
                counter(footnote).update(n => n - 1)
              }]
            #(
              if subtitle != none {
                parbreak()
                text(font: ("Libertinus Serif", "New York", "Times New Roman"), weight: "semibold", size: 1.25em, hyphenate: false)[#subtitle]
              }
             )])
      }

      #if authors != none and authors != [] {
        let count = authors.len()
        let ncols = calc.min(count, 3)
        grid(
          columns: (1fr,) * ncols,
          row-gutter: 1.5em,
          ..authors.map(author => align(center)[
            #author.name \
            #author.affiliation \
            #author.email
          ])
        )
      }

      #if date != none {
        align(center)[#block(inset: 1em)[
            #date
          ]]
      }

      #if abstract != none {
        block(inset: 2em)[
          #text(weight: "semibold")[#abstract-title] #h(1em) #abstract
        ]
      }
    ])
  }
  doc
}
#show: doc => conf(
  title: [Resisting AI Sycophancy in Open-Ended Research: Reconstructing Decision Inquiry with Constraint Optimization],
  subtitle: [A Running Example: "Is Nvidia Worth Buying at the Current Stage?"],
  authors: (
    ( name: [https://github.com/GoatGit],
      affiliation: "",
      email: "" ),
    ),
  abstract-title: [Abstract],
  margin: (top: 2.2cm, bottom: 2.2cm, x: 2.2cm),
  paper: "a4",
  font: ("Libertinus Serif", "New York", "Times New Roman"),
  fontsize: 10.5pt,
  codefont: ("Libertinus Serif", "New York", "Times New Roman"),
  lang: "en",
  region: "US",
  sectionnumbering: none,
  pagenumbering: "1",
  cols: 1,
  doc,
)

#outline(
  title: [Contents],
  depth: 2
);

#pagebreak()

== Abstract
<abstract>
This paper examines a core risk in open-ended research: AI sycophancy
toward humans. Sycophancy is not merely pleasant wording, nor is it
simply factual error. It is the tendency of an AI system to
over-accommodate a user's question frame, emotional stance, or a
socially popular narrative, to mistake the user's initial direction for
the true objective function, and therefore to converge too early on a
conclusion that appears complete but is in fact fragile. Using "whether
Nvidia is worth buying at the current stage" as a running example, the
user appears to be asking for investment research, but the prompt also
gives the AI a directional starting point: Nvidia is an AI leader, the
market narrative is strong, and public attention is high. As a result,
"worth buying" can easily become the candidate answer that the model
tries to prove or gently support.

This paper proposes a general method: reconstruct open-ended research
from "answer generation" into "decision optimization under constraints."
Before converging on a conclusion, an agent should first rebuild the
objective function, constraints, boundaries between facts and
assumptions, implied expectations, counterfactual scenarios, adversarial
arguments, and update rules. Nvidia is only the running case. The same
framework also applies to product opportunities, market entry, technical
choices, open-source project comparisons, and due diligence.

The paper makes three contributions. First, it gives an operational
definition of AI sycophancy in open-ended research: accepting the user's
original question as the objective function and optimizing the answer
toward a local optimum that the user is more likely to accept. Second,
it uses constraint optimization, robust optimization, sensitivity
analysis, and Bayesian updating to explain how to resist that local
optimum. Third, it formalizes multi-round research as residual-driven
evidence iteration: in a discrete state space, it defines question,
constraint, evidence, hypothesis, adversarial, sensitivity, and action
residuals, then uses value of information and hard constraints to decide
when to continue research and when to move into a final report.

Keywords: AI sycophancy; open-ended research; constraint optimization;
robust decision-making; Bayesian updating; counterfactual analysis;
decision trees

= 1. Research Question and Basic Position
<research-question-and-basic-position>
This paper is not about whether Nvidia itself should be bought. The
value of the case is that it exposes a common bias in open-ended
research.

The user's question is:

#quote(block: true)[
Conduct deep research on whether Nvidia's stock is worth buying at the
current stage.
]

There is nothing wrong with this question, but it naturally carries
several risks:

#figure(
  align(center)[#table(
    columns: (50%, 50%),
    align: (auto,auto,),
    table.header([Implied premise], [Possible bias],),
    table.hline(),
    [Nvidia deserves focused research], [Other assets or alternatives
    with better risk-reward may be ignored],
    [Buying is currently a plausible action], ["Whether to buy" becomes
    the default goal instead of first defining the investment
    objective],
    [Deep research can produce a clear buy / do-not-buy
    answer], [Probabilities, scenarios, and user constraints may be
    ignored],
    [A strong company is worth buying], [Object quality is confused with
    action attractiveness],
    [AI can make the decision for the user], [Time horizon, position
    size, risk tolerance, and opportunity cost are ignored],
  )]
  , kind: table
  )

The core research questions of this paper are therefore:

+ Why does open-ended research easily induce AI systems to follow the
  user's question rather than reconstruct it?
+ How can the task of "giving an answer" be converted into the task of
  "building a decision system"?
+ What process allows an agent to keep updating across multiple research
  rounds instead of making a conclusion first and then searching for
  support?
+ How can we evaluate whether a research report truly serves a human
  decision-maker rather than merely leaving behind an audit trail of
  agent activity?

The basic position of this paper is that the world is random, noisy, and
not reliably predictable. The goal of research is not to manufacture
certainty, but to improve judgment under uncertainty. A good agent
should not place the bet for the user. It should help the user identify
the objective, constraints, evidence strength, key assumptions,
falsification conditions, and action boundaries.

= 2. Conceptual Definitions
<conceptual-definitions>
== 2.1 AI Sycophancy
<ai-sycophancy>
In this paper, AI sycophancy does not mean politeness, personalization,
or friendly expression. It refers to a failure of truth-tracking: in
order to accommodate the user's question, preference, emotion, or
mainstream narrative, the model reduces its loyalty to facts,
counterevidence, constraints, and uncertainty.

In open-ended research, AI sycophancy often appears as:

+ Accepting the user's original wording as the final objective function.
+ Prioritizing evidence that supports the direction implied by the user.
+ Packaging popular narratives as facts.
+ Quickly converging with language such as "although there are risks,
  the overall outlook is positive."
+ Omitting constraints that would change the action recommendation.
+ Failing to list new evidence that could falsify the conclusion.

For example, "Nvidia is an AI leader, so it deserves long-term attention
and can be bought in tranches" sounds balanced. But without implied
valuation expectations, downside scenarios, position constraints, and
opposing evidence, it may still be a local-optimum answer.

== 2.2 Open-Ended Research
<open-ended-research>
Open-ended research refers to research tasks whose objectives,
boundaries, evidence standards, and decision variables are not fully
clear at the start. It differs from pure fact retrieval.

A fact-retrieval question asks:

#quote(block: true)[
What was Nvidia's revenue in the latest quarter?
]

An open-ended research question asks:

#quote(block: true)[
Is Nvidia worth buying at the current stage?
]

The latter first requires answers to several questions: Who is buying?
For how long? How much? What drawdown can they tolerate? What
alternatives are being compared? What evidence would change the
judgment? Without these constraints, the word "worth" has no stable
meaning.

== 2.3 Constraint Optimization
<constraint-optimization>
This paper formalizes open-ended research as a constrained
decision-optimization problem:

$ max_a U(a | E, H, C) - lambda R(a) - gamma I(a) $

where:

- $a$ is a candidate action, such as buy, wait, buy in tranches, avoid,
  or continue researching;
- $U(a | E, H, C)$ is the utility of the action under evidence
  $E$, hypotheses $H$, and constraints $C$\;
- $R\(a\)$ is risk, including drawdown, failure probability, opportunity
  cost, and irreversible loss;
- $I\(a\)$ is the uncertainty cost caused by insufficient information;
- $lambda$ and $gamma$ are the user's penalty weights for risk and
  uncertainty.

In the Nvidia case, the action variable is not "give a bullish or
bearish view." The real action variables include:

- whether to initiate a new position;
- if buying, how much to buy;
- whether to buy all at once or in tranches;
- whether existing holders should continue holding;
- what price or evidence should trigger reassessment;
- whether there are better alternative assets.

= 3. Related Work and Theoretical Anchors
<related-work-and-theoretical-anchors>
This paper does not mechanically impose mathematical optimization
concepts on research tasks. Instead, it borrows several mature research
traditions as theoretical anchors.

== 3.1 Language-Model Sycophancy
<language-model-sycophancy>
Existing studies have shown that language models may tend to accommodate
user views, especially in subjective questions, value judgments, or
tasks involving user preferences. Such phenomena are often related to
human-feedback training, preference learning, and reward signals for
"appearing helpful." For open-ended research, the risk is not only that
the model states incorrect facts. The deeper risk is that the model
over-conforms to the question frame: the user gives a directional
question, and the model follows that direction to generate an apparently
sufficient answer.

== 3.2 Robust Optimization and Sensitivity Analysis
<robust-optimization-and-sensitivity-analysis>
Robust optimization asks how to find a plan that does not collapse when
parameters are uncertain, the model is imperfect, or the environment
changes. Open-ended research faces a similar problem. If a conclusion
only holds when AI capital expenditure continues to grow rapidly, gross
margins remain high, valuation multiples do not compress, and market
risk appetite stays unchanged, it is not a robust conclusion.

Therefore, a research report must perform sensitivity analysis:

- Which variables most affect the conclusion?
- How much must those variables change before the action recommendation
  changes?
- What evidence can move the judgment from "observe" to "buy"?
- What evidence would invalidate the core logic?

== 3.3 Bayesian Updating and Forecast Calibration
<bayesian-updating-and-forecast-calibration>
Open-ended research should not make a one-shot final judgment. A better
approach is to write the judgment as an updatable hypothesis system:
which hypotheses the current evidence supports, what confidence level
they carry, what is most worth observing next, and what evidence would
move the probability upward or downward.

This is consistent with Bayesian updating:

$ P(H | E) = frac(P(E | H) P(H), P(E)) $

A research report does not need to assign precise probabilities to every
judgment, but it should reason probabilistically: the conclusion is
conditional, revisable, and dependent on evidence strength.

== 3.4 Decision Analysis
<decision-analysis>
Human decision-makers ultimately need action meaning, not piles of
material. Decision analysis requires a report to convert evidence into:

- optional actions;
- the benefits and risks of each action;
- trigger conditions;
- decision trees;
- review and update rules.

This is also the core principle of this paper: a research report is a
judgment memo for human decision-makers, not an audit log of an agent's
work.

== 3.5 Operationalizing Mathematical Methods
<operationalizing-mathematical-methods>
This paper uses mathematical optimization not to create an illusion of
precision, but to give open-ended research an anti-bias language.
Real-world decisions cannot be fully described by a single formula. But
formulas can remind the agent that objectives, constraints, risks,
uncertainty, and opportunity costs must enter the judgment at the same
time.

=== 3.5.1 Initial Points and Local Optima
<initial-points-and-local-optima>
In numerical optimization, many algorithms start from an initial point
$x_0$. When the objective function is non-convex, different initial
points may lead to different local optima. Open-ended research is
similar:

$ x_0 = upright("the user’s original wording") + upright("the user’s emotion") + upright("social narrative") + upright("model compliance tendency") $

If the user asks:

#quote(block: true)[
As an AI leader, is Nvidia still worth buying now?
]

This initial point is clearly bullish. An agent can easily converge
along the following path:

$ upright("AI leader") arrow.r upright("high growth") arrow.r upright("strong moat") arrow.r upright("long-term optimism") arrow.r upright("buy") $

If the user asks:

#quote(block: true)[
Has Nvidia's valuation already priced in the next ten years of growth?
]

The agent may instead converge along a bearish path. Both answers may be
logically coherent, but each is only a local solution reached from a
different initial point. The first step in anti-sycophantic research is
therefore not to mistake the user's starting point for the objective
function itself.

=== 3.5.2 Multi-Start Search
<multi-start-search>
The idea of multi-start search is to begin from multiple initial points
and compare the solutions reached by different paths. In research, this
means asking the agent to analyze from the perspectives of a bull, a
bear, a neutral observer, a risk manager, a long-term investor, and a
short-term trader. The value of multiple perspectives is not to average
them. It is to discover whether the conclusion is sensitive to the
initial stance.

If the bullish perspective says "buy," the bearish perspective says
"valuation is excessive," and the risk manager says "portfolio exposure
is already too concentrated," the final question is no longer "who is
right?" It becomes:

- What evidence distinguishes these explanations?
- Which variable is most likely to determine the result?
- When evidence is insufficient, which action minimizes loss?

=== 3.5.3 Random Perturbation and Counterfactuals
<random-perturbation-and-counterfactuals>
Perturbation in optimization is used to test the stability of a
solution. Counterfactual perturbation in research is used to test
whether a conclusion depends on a single fragile assumption.

For example, a conclusion to "buy Nvidia" may depend on the following
assumptions:

- AI capital expenditure continues to grow rapidly;
- cloud providers do not materially reduce GPU purchases;
- gross margins remain high;
- competitors and in-house chips do not become meaningful substitutes;
- current valuation multiples do not compress significantly.

Counterfactual perturbation requires changing these parameters one by
one and observing whether the action recommendation changes. If a
conclusion holds only when all optimistic assumptions hold at the same
time, its robustness is weak.

=== 3.5.4 Sensitivity Analysis
<sensitivity-analysis>
Sensitivity analysis answers which variable changes can most alter the
conclusion. In an investment case, a simplified model can be used:

$ P = upright("EPS")_(upright("fwd")) times upright("PE")_(upright("fwd")) $

Then the stock-price change can be decomposed as:

$ Delta P approx upright("PE")_(upright("fwd")) dot.op Delta upright("EPS")_(upright("fwd")) + upright("EPS")_(upright("fwd")) dot.op Delta upright("PE")_(upright("fwd")) $

This expression reminds us that even if EPS is revised upward, the stock
price may still fall if the PE multiple compresses by more. In
open-ended research, sensitivity analysis does not necessarily require
complex formulas, but it must identify the "conclusion levers":

- in product research, the most sensitive variables may be customer
  acquisition cost, retention, or paid conversion;
- in technical selection, the most sensitive variables may be team
  learning cost, ecosystem maturity, or migration cost;
- in open-source evaluation, the most sensitive variables may be
  maintainer activity, license risk, or critical dependencies;
- in investment research, the most sensitive variables may be profit
  growth, valuation multiples, capital flows, or policy constraints.

=== 3.5.5 Inverse Problems and Implied Expectations
<inverse-problems-and-implied-expectations>
Many open-ended research tasks cannot only ask "is this object good?"
They must also reverse-engineer "what expectation does the current
choice imply?" This is an inverse problem.

In the Nvidia case, if the current price is to deliver a target
annualized return, then future EPS, valuation multiples, and the
duration of growth must satisfy certain conditions:

$ P_T^* = P_0 times (1 + r)^T $

$ upright("EPS")_T^* = frac(P_T^*, upright("PE")_T^(upright("exit"))) $

If the reverse calculation shows that the future must maintain very high
growth and a high valuation multiple for a long time, then a "buy"
recommendation requires stronger evidence. The same method applies to
other research:

- Entering a market implies what customer acquisition cost and
  conversion rate?
- Adopting a technology stack implies what learning curve and
  maintenance cost?
- Choosing an open-source project implies what level of continued
  community maintenance and security response?

=== 3.5.6 Robust Optimization and Minimax
<robust-optimization-and-minimax>
Robust optimization does not pursue a single best outcome. It pursues an
action that remains acceptable across multiple adverse scenarios. In
open-ended research, the best recommendation is often not to maximize
optimistic upside, but to choose a plan with lower regret, stronger
updatability, and greater reversibility.

In the Nvidia case, a robust action may be neither "buy with the whole
portfolio" nor "avoid entirely," but instead:

- test with a small position;
- wait for earnings or a valuation pullback;
- set reassessment conditions for existing holders;
- reduce single-name risk through portfolio construction;
- define the evidence that would trigger adding or reducing exposure.

This kind of output is less exciting than a one-sentence conclusion, but
it is closer to real decision-making.

=== 3.5.7 Regularization
<regularization>
In machine learning, regularization reduces overfitting. In open-ended
research, regularization prevents an agent from overfitting to popular
narratives, user preferences, or recent data.

Popular narratives in the Nvidia case include:

- the AI revolution;
- compute as an unavoidable need;
- the "picks and shovels" story;
- the CUDA moat;
- global GPU dominance;
- the certainty of long-term growth.

These narratives may have a factual basis. But if a report develops only
along these narratives, it overfits. Anti-narrative regularization
requires the agent to actively introduce:

- valuation constraints;
- competitive substitution;
- customer concentration;
- interest rates and risk appetite;
- the capital-expenditure cycle;
- conditions that could falsify the conclusion.

=== 3.5.8 Bayesian Updating
<bayesian-updating>
Bayesian updating emphasizes that judgments change with new evidence.
The conclusion of open-ended research should not be written as a
permanent judgment, but as a conditional one.

$ P(H | E) prop P(H) times P(E | H) $

In a report, this can be translated into three kinds of content:

+ Current judgment: based on existing evidence, which explanation is
  strongest?
+ Update rules: what new evidence would raise or lower confidence?
+ Stopping conditions: when can a final report be formed, and when must
  research continue?

This is also the theoretical basis for the quality gate in multi-round
research. If the quality score is insufficient, or if the current
evidence still points toward more research, a report should not stop
merely because it has produced an elegant conclusion.

=== 3.5.9 Decision Trees
<decision-trees>
A decision tree converts uncertainty into conditional action. It does
not require the agent to predict a single future. It requires the agent
to state what should be done under different states.

Open-ended research should move from:

I think A is better.

to:

If evidence E1 appears, take action A; if evidence E2 appears, take
action B; if key hypothesis H is falsified, stop or pivot; if
decision-level evidence is still missing, enter the next research round.

Decision trees significantly reduce sycophancy risk because they force
the agent to write the conclusion as a testable, updatable, executable
conditional system.

== 3.6 Mapping of Methods
<mapping-of-methods>
In mathematical optimization, the following methods can help avoid local
optima:

- multi-start search;
- global optimization;
- simulated annealing;
- sensitivity analysis;
- robust optimization;
- Bayesian updating;
- adversarial testing;
- regularization;
- scenario analysis.

Mapped to AI-assisted investment research, they become:

#figure(
  align(center)[#table(
    columns: (50%, 50%),
    align: (auto,auto,),
    table.header([Mathematical optimization method], [Corresponding
      method in AI investment research],),
    table.hline(),
    [Redefining the objective function], [Do not ask "buy or not"\;
    first ask what the investment objective, time horizon, position
    size, and constraints are],
    [Multi-start search], [Analyze from bullish, bearish, neutral,
    risk-manager, and long-term-investor perspectives],
    [Global search], [Do not validate a single candidate conclusion;
    compare buying, waiting, holding, trimming, and alternative assets],
    [Simulated annealing], [In early stages, allow unconventional
    explanations and weak signals; later converge gradually according to
    evidence strength],
    [Random perturbation], [Change key assumptions, such as slower AI
    demand, lower gross margins, or tighter export restrictions],
    [Sensitivity analysis], [Test how changes in revenue growth, profit
    margin, EPS, and PE multiples affect the stock price and action
    recommendation],
    [Adversarial testing], [Make the AI actively refute its own bullish
    or bearish conclusions and identify the weakest assumptions],
    [Regularization], [Prevent overfitting to popular narratives, recent
    price trends, and the user's original preference],
    [Bayesian updating], [Dynamically update the judgment as earnings,
    orders, competition, and capex data change],
    [Robust optimization], [Find an investment strategy that is not too
    bad across several scenarios, is more reversible, and has lower
    regret],
    [Scenario analysis], [Construct optimistic, base, bearish, and
    stress scenarios instead of predicting a single future],
    [Decision tree], [Output conditional actions, triggers, and review
    rules instead of a single conclusion],
  )]
  , kind: table
  )

This mapping can also be generalized beyond investment research. Product
opportunities correspond to market entry and resource allocation.
Technical choices correspond to architecture constraints and migration
cost. Open-source evaluation corresponds to maintenance risk and
adoption boundaries. The core remains the same: first reconstruct the
objective function, then perform multi-path search, counterfactual
stress testing, and conditional action output.

== 3.7 Residual-Driven Evidence Iteration: A Generalized Descent Theory for Open-Ended Research
<residual-driven-evidence-iteration-a-generalized-descent-theory-for-open-ended-research>
The preceding discussion is enough to show that open-ended research is
not the minimization of a differentiable loss function. It is the
continuous compression of decision residuals in a discrete state space
formed by questions, constraints, evidence, hypotheses, and actions.
This section gives only the formal language: state, residuals,
operators, descent direction, and stopping conditions. How to execute
one iteration is developed in Chapter 5. To write this iteration in a
more unified theory, the research state at round $t$ can be denoted as:

$ x_t = (Q_t, C_t, F_t, E_t, H_t, A_t, J_t) $

where $Q_t$ is the question statement, $C_t$ is the constraint set,
$F_t$ is the research framework, $E_t$ is the evidence set, $H_t$ is the
set of candidate hypotheses, $A_t$ is the set of candidate actions, and
$J_t$ is the current judgment. This state is not an ordinary real-valued
vector. It is a composite object carrying semantics, evidence, and
decisions.

=== 3.7.1 Residual Vector
<residual-vector>
Research quality can be written as a residual vector:

$ r(x_t) = (r_q, r_c, r_e, r_h, r_a, r_s, r_j) $

where:

- $r_q$: question residual, whether the original question has been
  wrongly accepted;
- $r_c$: constraint residual, whether time horizon, budget, risk,
  position size, and responsibility boundaries are missing;
- $r_e$: evidence residual, whether key claims lack direct evidence;
- $r_h$: hypothesis residual, whether core hypotheses remain fragile;
- $r_a$: adversarial residual, whether the strongest opposing argument
  has been handled;
- $r_s$: sensitivity residual, whether the variables that would change
  the conclusion remain unclear;
- $r_j$: action residual, whether the reader still does not know what to
  do.

Let $w_i gt.eq 0$ be the weight of each residual component under a given
task. The total residual can be written as:

$ Phi(x_t) = sum_i w_i r_i(x_t) $

Its meaning is simple: research is not a contest of length, but a
contest of how many key residuals remain uncompressed. The weights are
not meant to make scoring look precise. They let task-specific risk
differences enter the judgment. For example, high-risk tasks place more
weight on evidence, constraints, and responsibility boundaries, while
low-risk creative tasks may tolerate higher uncertainty.

=== 3.7.2 Non-Commutative Operators and Process Order
<non-commutative-operators-and-process-order>
From an algebraic point of view, question projection, evidence
observation, multi-path expansion, adversarial testing, synthesis
updating, and direction selection can be viewed as operators acting on
the state space $cal(X)$. Under composition, they form a non-commutative
semigroup: order is not an implementation detail, but a theoretical
property. Research-then-redteam and redteam-then-research do not produce
the same state.

One round can be written as:

$ x_(t + 1) = V compose S compose A compose G compose M_E compose Pi_C(x_t) $

where:

- $Pi_C$ is the projection operator that projects the question back into
  real constraints;
- $M_E$ is the observation operator that collects and updates evidence;
- $G$ is the multi-start operator that expands candidate paths again;
- $A$ is the adversarial operator that attacks the strongest current
  argument;
- $S$ is the synthesis-update operator that compresses the evidence and
  opposition back into judgment;
- $V$ is the direction-selection operator that decides which residual
  direction to iterate along next.

This also explains why open-ended research cannot form a conclusion
first and then retrospectively add a framework, evidence, and opposing
argument. That is not iteration. It is only an after-the-fact audit.

=== 3.7.3 Generalized Descent Direction
<generalized-descent-direction>
If traditional gradient descent moves along $- nabla L\(x\)$ in a
continuous space, the descent direction in this paper is more like "the
next step that reduces the residual most per unit cost." Formally:

$ d_t = arg max_(d in cal(D)) frac(bb(E)[Phi(x_t) - Phi(T_d(x_t))], upright("Cost")(d)) $

where $T_d$ denotes a candidate research action and $cal(D)$ is the set
of all available actions. This definition does not claim that we can
compute an exact gradient. It says that the next round should prioritize
the evidence direction most likely to reduce judgment residuals.

Thus, residual-driven evidence iteration is closer to a combination of
generalized coordinate descent, projected search, and trust-region
updating in a discrete state space than to traditional gradient descent.
It borrows the intuition of descent methods without depending on a
differentiable loss function.

=== 3.7.4 Stopping Conditions and Value of Information
<stopping-conditions-and-value-of-information>
Open-ended research should not iterate forever. The stopping condition
is not "a lot has been written," but:

$ Phi(x_t) <= epsilon quad upright("and") quad upright("VOI")(d_t) < upright("Cost")(d_t) $

where $upright("VOI")(d_t)$ is the expected value of information of
the next research action $d_t$: the likely benefit of changing the
action recommendation, reducing major uncertainty, or correcting a wrong
judgment. In other words, when remaining residuals are below the
threshold and the expected information value of the next round is lower
than the cost of continuing research, the process should stop and move
into the final report. The quality gate is therefore only a coarse
observation of residuals, not the objective function itself. If the
quality score becomes the target, the model is more likely to optimize
toward attractive audit tables rather than better judgment.

=== 3.7.5 Correspondence with the Research Process
<correspondence-with-the-research-process>
This theoretical framework corresponds to a general multi-round research
process. The mapping here is only an operator-level abstraction; the
concrete execution steps are developed in Chapter 5:

- question projection: pull the original question back to the true
  objective function;
- evidence observation: collect direct evidence and compress the
  evidence residual;
- multi-path expansion: expand the search space again to avoid local
  optima;
- adversarial testing: find the biggest weakness in the current
  solution, analogous to estimating the steepest residual direction;
- synthesis updating: compress evidence, opposing arguments, and
  scenarios into a conditional judgment;
- direction selection: choose the next descent direction, or stop when
  value of information is insufficient.

Therefore, the core iteration in this paper is not "write another
round." It is "update one round along the direction that most reduces
decision residuals." This is the minimal mathematical abstraction of
open-ended research.

= 4. Method: From Answer Generation to Decision Optimization
<method-from-answer-generation-to-decision-optimization>
The following section gives a general process. It can be used for
investment research, product research, market research, technology
selection, open-source evaluation, and due diligence. Each method
includes three parts: a method explanation, the Nvidia case, and an
example prompt.

== 4.1 Reconstruct the Objective Function
<reconstruct-the-objective-function>
Original question:

#quote(block: true)[
Is Nvidia worth buying now?
]

The implied objective function can easily become:

$ max S_(upright("buy")) $

This induces the agent to search for reasons to "buy" or "not buy." A
better objective function is:

$ max bb(E)[R] - lambda cal(R) - gamma cal(U) - eta cal(O) $

The question is therefore reconstructed as:

#quote(block: true)[
Under current price, valuation, market expectations, AI compute demand,
competitive structure, and my investment-horizon constraints, is
Nvidia's risk-adjusted expected return attractive? If action is taken,
what position size, waiting conditions, and risk controls are
reasonable?
]

This reconstruction is the first anti-sycophancy move: the agent no
longer treats the user's sentence as the objective function, but first
examines what the user is really trying to optimize.

In the Nvidia case, "whether it is worth buying" can correspond to at
least four different objectives:

#figure(
  align(center)[#table(
    columns: (50%, 50%),
    align: (auto,auto,),
    table.header([Objective], [More precise question],),
    table.hline(),
    [Long-term compounding], [If held for 5-10 years, can Nvidia provide
    high-quality compounding?],
    [Risk-adjusted return], [At the current price, does upside
    compensate for drawdown risk?],
    [Short-term trading], [Over the next earnings cycle, do expectation
    gaps and capital flows support a trade?],
    [Portfolio allocation], [Given existing technology-stock exposure,
    does adding Nvidia improve the portfolio?],
  )]
  , kind: table
  )

Example prompt:

Please do not answer "buy / do not buy" yet. Reconstruct this question
as a decision-optimization problem: 1. What objectives might I really be
optimizing? 2. What constraints correspond to each objective? 3. If
investment horizon, position size, and risk tolerance are missing, how
should you handle them? 4. Give a more rigorous question statement than
"is it worth buying?"

== 4.2 Split Facts, Assumptions, Inferences, and Value Judgments
<split-facts-assumptions-inferences-and-value-judgments>
The most common error in open-ended research is presenting assumptions
as facts.

#figure(
  align(center)[#table(
    columns: (50%, 50%),
    align: (auto,auto,),
    table.header([Type], [Example in the Nvidia case],),
    table.hline(),
    [Fact], [Nvidia is one of the global leaders in GPUs and AI
    accelerators],
    [Data to verify], [Current valuation, latest revenue, gross margin,
    free cash flow, analyst expectations],
    [Assumption], [AI capital expenditure will continue to grow rapidly
    in the next several years],
    [Inference], [Nvidia's profit will continue to grow rapidly],
    [Value judgment], [The current valuation is still reasonable],
    [Action recommendation], [Buy, wait, hold, trim, or avoid],
  )]
  , kind: table
  )

A reliable report should let readers clearly see which statements are
evidence, which are merely assumptions to be verified, and which are the
author's inferences.

In the Nvidia case, the following sentences are often mixed together:

#figure(
  align(center)[#table(
    columns: (50%, 50%),
    align: (auto,auto,),
    table.header([Sentence], [More accurate classification],),
    table.hline(),
    [Nvidia's data-center business has grown significantly in recent
    years], [Historical fact, but still needs verification against the
    latest financial report],
    [AI inference will take over from training as the next long-term
    growth driver], [Assumption],
    [The CUDA ecosystem is hard to replace in the short
    term], [Inference requiring evidence from developers, customers, and
    migration costs],
    [A high valuation can be absorbed by high growth], [Value judgment
    requiring reverse-engineering of implied expectations],
    [If you do not buy now, it will be more expensive later], [Emotional
    narrative, not evidence],
  )]
  , kind: table
  )

Example prompt:

Please split my question into six layers: 1. known facts; 2. data
requiring real-time lookup; 3. market consensus; 4. key assumptions that
have not yet been verified; 5. subjective judgments or popular
narratives; 6. missing information that could change the action
recommendation.

Do not write assumptions as facts. For every core judgment, state which
layer it belongs to.

== 4.3 Distinguish Object Quality from Action Attractiveness
<distinguish-object-quality-from-action-attractiveness>
"A good company" does not automatically mean "a good stock." More
generally, "a good object" does not automatically imply "a good action."

#figure(
  align(center)[#table(
    columns: (50%, 50%),
    align: (auto,auto,),
    table.header([Question], [Focus],),
    table.hline(),
    [Is Nvidia a good company?], [Technology, moat, business model,
    financial quality, growth runway],
    [Is Nvidia a good stock at the current stage?], [Current price,
    implied expectations, upside, downside risk, opportunity cost],
  )]
  , kind: table
  )

This distinction generalizes to other fields:

- a good product does not necessarily mean a market is worth entering;
- a good technology does not necessarily mean a stack is worth adopting;
- a good open-source project does not necessarily fit the current team;
- a good company does not necessarily deserve investment now.

As a company, Nvidia may have strong technology, a strong ecosystem,
strong financial quality, and a large growth runway. As a stock, it must
still face current valuation, market expectations, crowded positioning,
the interest-rate environment, position constraints, and opportunity
cost. Object quality answers "is it good?" Action attractiveness answers
"is doing this now worthwhile?"

Example prompt:

Please answer two questions separately: 1. Is Nvidia an excellent
company? Analyze business model, technical barriers, financial quality,
and industry runway. 2. Is Nvidia currently a stock worth buying?
Analyze current price, implied expectations, risk-reward, opportunity
cost, and position constraints.

Please state which conclusions support only "the company is excellent"
and which conclusions can support "the current action is attractive."

== 4.4 Multi-Start Search
<multi-start-search-1>
To avoid convergence along a single path, the agent should begin from
multiple starting points.

In the Nvidia case, the perspectives should at least include:

+ Bullish fund manager: why can it still rise?
+ Bearish researcher: where is the market too optimistic?
+ Neutral sell-side analyst: which metrics most affect consensus
  expectations?
+ Long-term value investor: are free cash flow and margin of safety
  sufficient?
+ Growth investor: can growth continue to digest the valuation?
+ Short-term trader: how do flows, trend, and earnings volatility look?
+ Risk manager: can portfolio exposure and maximum drawdown be
  tolerated?

Multiple perspectives are not a call for bland balance. They are a way
to expose each view's blind spots.

Typical focus areas in the Nvidia case are:

#figure(
  align(center)[#table(
    columns: (33.33%, 33.33%, 33.33%),
    align: (auto,auto,auto,),
    table.header([Perspective], [Opportunity it may see], [Risk it may
      ignore],),
    table.hline(),
    [Bullish fund manager], [AI compute demand, CUDA ecosystem,
    Blackwell cycle], [Valuation and crowded positioning],
    [Bearish researcher], [Slowing capex, falling gross margin, in-house
    chip substitution], [Continued upside surprise from technical
    leadership],
    [Neutral analyst], [Earnings guidance, EPS revisions, supply-chain
    bottlenecks], [Extreme scenarios],
    [Long-term value investor], [Moat and cash flow], [Insufficient
    current margin of safety],
    [Growth investor], [TAM expansion and new growth curves], [Valuation
    compression after growth slows],
    [Short-term trader], [Trend, flows, earnings volatility], [Long-term
    changes in fundamentals],
    [Risk manager], [Position size, correlation, maximum
    drawdown], [Excessive conservatism leading to missed upside],
  )]
  , kind: table
  )

Example prompt:

Please analyze the same question from seven perspectives: bullish fund
manager, bearish researcher, neutral sell-side analyst, long-term value
investor, growth investor, short-term trader, and risk manager.

For each perspective, state: 1. the core judgment; 2. the most important
evidence; 3. the variable that is most concerning; 4. the current action
recommendation; 5. the error that this perspective itself is most likely
to make.

Finally, compare which disagreements come from different facts and which
come from different objective functions.

== 4.5 Counterfactual Perturbation
<counterfactual-perturbation>
A conclusion is robust only if it still stands after key assumptions are
perturbed.

Key counterfactuals in the Nvidia case include:

- What if AI capital expenditure slows?
- What if major customers accelerate in-house chip substitution?
- What if gross margins decline?
- What if Blackwell demand continues to exceed expectations?
- What if export controls or geopolitical constraints intensify?
- What if rising macro interest rates compress growth-stock valuations?

Each counterfactual must answer three questions: which evidence changes,
which assumptions change, and what action changes.

Five key counterfactuals in the Nvidia case can be expanded as follows:

#figure(
  align(center)[#table(
    columns: (33.33%, 33.33%, 33.33%),
    align: (auto,auto,auto,),
    table.header([Counterfactual], [Impact path], [Action implication],),
    table.hline(),
    [AI capex slows], [Data-center revenue growth is revised downward;
    the market revalues TAM], [Avoid chasing; wait for order and
    guidance validation],
    [Gross margin declines], [Profit elasticity falls; EPS expectations
    are revised downward], [Valuation center may move lower],
    [In-house chip substitution accelerates], [Customer-concentration
    risk rises; bargaining power declines], [Reduce the long-term
    monopoly assumption],
    [Blackwell demand exceeds expectations], [EPS revisions rise;
    supply-demand tightness continues], [Increase the weight of the
    optimistic scenario],
    [Export controls intensify], [Some markets are restricted; product
    mix changes], [Reassess regional revenue and margins],
  )]
  , kind: table
  )

Example prompt:

Please run a counterfactual stress test on the current conclusion. At
least discuss: 1. AI capital expenditure slows; 2. gross margin
declines; 3. cloud providers accelerate in-house chip substitution; 4.
the new product cycle exceeds expectations; 5. export controls or
regulatory constraints intensify; 6. rising macro interest rates
compress growth-stock valuations.

For each counterfactual, explain the impact on revenue, margins,
valuation multiples, stock-price range, and action recommendation.

== 4.6 Sensitivity Analysis
<sensitivity-analysis-1>
Sensitivity analysis should identify the variables that truly determine
success or failure. Without it, a report tends to list every factor
flatly, leaving readers unable to tell what matters most.

In the Nvidia case, key variables include at least:

+ data-center revenue growth;
+ gross margin;
+ operating expense ratio;
+ EPS growth;
+ forward PE;
+ sustainability of AI capital expenditure;
+ major-customer concentration;
+ speed of competitive substitution;
+ market risk appetite;
+ interest-rate level.

A simplified framework is:

$ P_(upright("future")) = upright("EPS")_(upright("fwd")) times upright("PE")_(upright("fwd")) $

This yields three typical scenarios:

#figure(
  align(center)[#table(
    columns: (25%, 25%, 25%, 25%),
    align: (auto,auto,auto,auto,),
    table.header([Scenario], [EPS], [PE], [Possible result],),
    table.hline(),
    [Bullish], [Revised upward], [Stable or slightly expanding], [Stock
    continues to rise],
    [Base], [Slightly revised upward], [Slightly compressed], [Limited
    return with high volatility],
    [Bearish], [Revised downward], [Compressed], [EPS and valuation both
    fall],
  )]
  , kind: table
  )

Example prompt:

Please perform sensitivity analysis and identify the variables that most
change the conclusion. At least analyze revenue growth, gross margin,
EPS growth, forward PE, AI capex, competitive substitution, export
controls, and macro interest rates.

Please provide optimistic, base, and bearish scenarios, and explain what
variable changes would move the recommendation from buy to observe, or
from observe to avoid.

== 4.7 Reverse-Engineering Valuation-Implied Expectations
<reverse-engineering-valuation-implied-expectations>
Valuation is not a static label. A high valuation does not necessarily
mean high risk, and a low valuation does not necessarily mean cheap. The
key question is what future the current price implies.

A simplified expression is:

$ P = upright("EPS")_(upright("fwd")) times upright("PE")_(upright("fwd")) $

If investors want a reasonable return, they must reverse-engineer:

- what level future EPS must reach;
- what exit PE must be maintained;
- how long growth must be realized;
- whether EPS growth can offset PE compression;
- how large downside could be if EPS is revised downward while PE
  compresses.

This step prevents the agent from substituting "the company is good" for
"the price is reasonable."

In the Nvidia case, one should not merely say "the PE is high" or "the
PE is not high." The report should reverse-engineer:

- If a 10% annualized return over the next three years is required, what
  revenue and EPS levels are needed?
- If the exit PE compresses, how fast must EPS grow to offset it?
- If the market already expects high growth, how large must the upside
  surprise be to produce further stock upside?
- Does the current valuation imply that gross margins will remain high
  for a long time?

Example prompt:

Please do not merely judge whether valuation is high or low.
Reverse-engineer the future expectations implied by the current price:
\1. What EPS level must the current price correspond to in three and
five years? 2. If investors require 10%, 15%, and 20% annualized
returns, what EPS CAGR and exit PE are required? 3. If PE compresses to
different levels, how does the stock-price range change? 4. Are current
market expectations already too optimistic?

== 4.8 Adversarial Validation
<adversarial-validation>
A report should generate both the strongest supporting argument and the
strongest opposing argument, rather than listing a few symbolic risks.

An adversarial process can be:

+ Write the strongest buying thesis.
+ Write the strongest non-buying thesis.
+ Identify the most fragile assumption on each side.
+ Judge which evidence is stronger and which evidence remains missing.
+ Give a conditional action instead of a single-path conclusion.

The purpose of adversarial validation is not to manufacture a moderate
conclusion. It is to make the conclusion withstand attack.

In the Nvidia case, the strongest buying thesis may be: AI compute
demand is still expanding; the company remains technically ahead; the
software ecosystem reinforces hardware stickiness; data-center business
may continue to surprise; and cash flow and margin quality are high. The
strongest non-buying thesis may be: current valuation implies very high
growth; customer capital expenditure may be cyclical; competition and
in-house chips may erode part of the market; export restrictions remain
a risk; and if performance merely meets rather than exceeds
expectations, the stock can still correct.

Example prompt:

Please perform three-part adversarial validation: 1. write the strongest
buying argument; 2. write the strongest non-buying argument; 3. speak as
the chair of an investment committee, identify the weakest assumptions
on both sides, and give a conditional conclusion after adversarial
testing.

Do not handle this by becoming blandly neutral. Clearly state the key
evidence that most needs verification now.

== 4.9 Bayesian Updating
<bayesian-updating-1>
A research conclusion should exist in the form "under current evidence"
and should include update rules.

#figure(
  align(center)[#table(
    columns: (25%, 25%, 25%, 25%),
    align: (auto,auto,auto,auto,),
    table.header([Hypothesis], [Current evidence], [Evidence that raises
      confidence], [Evidence that lowers confidence],),
    table.hline(),
    [AI capex continues to grow], [Cloud-provider capex and order
    signals], [Upward guidance revisions and better order
    visibility], [Capex slowdown and inventory buildup],
    [Gross margins remain high], [Product mix and supply-demand
    structure], [New products ramp while pricing remains
    stable], [Competition intensifies and customers gain bargaining
    power],
    [Valuation can be digested by growth], [EPS revision
    expectations], [EPS is revised upward faster than the stock price
    rises], [EPS is revised downward or PE compresses],
  )]
  , kind: table
  )

This step turns the report from a "conclusion document" into an
updatable judgment system.

Example prompt:

Please write the current judgment as an updatable hypothesis system: 1.
What are the main investment hypotheses? 2. How strong is the current
evidence for each hypothesis? 3. What data should be tracked later? 4.
What evidence would increase the probability of buying? 5. What evidence
would decrease the probability of buying? 6. What evidence would fully
invalidate the investment logic?

== 4.10 Scenario Analysis and Decision-Tree Output
<scenario-analysis-and-decision-tree-output>
The final report should translate research into action boundaries:

If valuation is reasonable and earnings expectations continue to be
revised upward: consider a small position or tranche-based allocation.

If the stock price rises faster than earnings expectations are revised
upward: observe and avoid chasing.

If AI capital expenditure slows: pause buying and reassess.

If gross margin or data-center growth deteriorates materially: reduce
position size or avoid.

If existing technology-stock exposure is already high: control position
size and prioritize correlation risk.

A decision tree is better suited to the real world than a one-sentence
conclusion because the real world changes.

Scenario analysis should not merely write "optimistic, base, bearish."
Each scenario should correspond to an actionable strategy.

#figure(
  align(center)[#table(
    columns: (33.33%, 33.33%, 33.33%),
    align: (auto,auto,auto,),
    table.header([Scenario], [Basic assumptions], [Operational
      implication],),
    table.hline(),
    [Bullish], [EPS keeps being revised upward, PE does not compress
    materially, AI capex is stable], [Consider a small position or
    tranche-based allocation],
    [Base], [Growth remains good but the expectation gap is limited;
    valuation compresses slightly], [Wait for a better price or new
    evidence],
    [Bearish], [Capex slows, gross margin declines, and PE
    compresses], [Avoid, trim, or reassess],
  )]
  , kind: table
  )

Example prompt:

Please do not give a single buy / do-not-buy conclusion. Output a
decision tree: 1. Under what conditions can it be bought? 2. Under what
conditions should one wait? 3. Under what conditions should one avoid
it? 4. If already holding, what should be done? 5. If not yet holding,
what signals should be awaited? 6. How should reasonable position size
be set? 7. What are the review and stop-loss conditions?

== 4.11 Add Personal Constraints
<add-personal-constraints>
Recommendations without user constraints often have little meaning. The
same security can imply completely different actions for different
investors.

#figure(
  align(center)[#table(
    columns: (50%, 50%),
    align: (auto,auto,),
    table.header([Investor type], [Possible conclusion],),
    table.hline(),
    [Long-term growth investor], [May accept volatility, but must verify
    long-term growth and valuation digestion],
    [Value investor], [May require a larger margin of safety],
    [Short-term trader], [Focuses more on earnings windows, trend, and
    flow behavior],
    [Conservative investor], [May not be suitable for high-volatility,
    high-valuation assets],
    [Investor already heavily exposed to AI], [Incremental portfolio
    value of adding exposure is lower],
    [Investor with no technology-stock exposure], [A small allocation
    may have diversification value],
  )]
  , kind: table
  )

Example prompt:

Please give action recommendations under different constraints: 1.
long-term growth investor; 2. value investor; 3. short-term trader; 4.
conservative investor; 5. aggressive investor; 6. investor already
heavily exposed to AI / semiconductors; 7. investor with no
technology-stock exposure.

For each type, state whether action is suitable, reasonable position
size, main risk, signals to wait for, and how to respond if the judgment
is wrong.

== 4.12 Regularization: Prevent Overfitting to Popular Narratives
<regularization-prevent-overfitting-to-popular-narratives>
Popular narratives can make an agent produce fluent but fragile answers.
Regularization works by actively adding variables that constrain the
narrative.

In the Nvidia case, regularization does not deny the AI industry trend.
It requires the report to handle:

+ whether valuation has already reflected optimistic expectations;
+ whether recent stock-price gains have pulled forward expectations;
+ whether the AI trend can translate into customer ROI;
+ whether major customers will reduce dependence on a single supplier;
+ whether gross margins can remain high for a long time;
+ whether macro interest rates and risk appetite support high
  valuations.

Example prompt:

Please add anti-narrative regularization to the current analysis: 1. do
not infer current buyability automatically from being a great company;
\2. do not extrapolate recent gains into future gains; 3. do not use the
broad AI trend as a substitute for valuation and expectation-gap
analysis; 4. actively list the strongest bearish evidence; 5. reduce
conclusion certainty when real-time data is missing; 6. clearly state
how position size, horizon, and risk tolerance change the
recommendation.

= 5. Iterative Method: Updating Research Along Residual Directions
<iterative-method-updating-research-along-residual-directions>
Chapter 4 discussed individual methods: reconstructing the objective
function, splitting facts and assumptions, counterfactual perturbation,
sensitivity analysis, adversarial validation, Bayesian updating, and
decision trees. These methods answer what each step should do. This
chapter discusses the iterative method: after one research round ends,
how should the next round be chosen, how should judgment be updated, and
when should the process stop?

== 5.1 Basic Loop of One Research Round
<basic-loop-of-one-research-round>
A complete iteration can be written in six steps:

+ Question projection: check whether the user's original question equals
  the true objective function.
+ Evidence observation: collect direct evidence around key claims rather
  than piling up material.
+ Multi-path expansion: search again from bullish, bearish, neutral,
  risk-manager, and final-decision-maker starting points.
+ Adversarial testing: attack the strongest current conclusion and find
  its most fragile assumption.
+ Synthesis updating: merge evidence, opposition, scenarios, and
  constraints into a conditional judgment.
+ Direction selection: decide which residual direction the next round
  should follow, or whether to stop.

The point of the loop is not "doing more rounds." Each round must
compress a clear decision residual. If a round only adds material,
expands paragraphs, or repeats the previous conclusion, it has not truly
descended.

== 5.2 Residual Diagnosis
<residual-diagnosis>
At the end of each round, the first question should be: what is the
largest residual in the current report?

#figure(
  align(center)[#table(
    columns: (33.33%, 33.33%, 33.33%),
    align: (auto,auto,auto,),
    table.header([Residual type], [Diagnostic question], [Next-round
      direction],),
    table.hline(),
    [Question residual], [Is the report still answering the user's
    original wording rather than the true objective
    function?], [Reconstruct the objective and clarify the action
    variable],
    [Constraint residual], [Are time horizon, budget, position size,
    risk tolerance, and responsibility boundaries missing?], [Add user
    constraints or provide constraint branches],
    [Evidence residual], [Does the most important claim lack direct
    evidence?], [Find primary sources, direct data, and conflicting
    evidence],
    [Hypothesis residual], [Does the core conclusion depend on
    unverified assumptions?], [Perform counterfactual perturbation and
    sensitivity analysis],
    [Adversarial residual], [Is the strongest opposition only a symbolic
    list of risks?], [Generate the strongest opposing argument and
    falsification conditions],
    [Sensitivity residual], [Are the variables that would change the
    conclusion still unclear?], [Identify conclusion levers and
    thresholds],
    [Action residual], [Does the reader still not know what to
    do?], [Output conditional recommendations, decision trees, and
    triggers],
  )]
  , kind: table
  )

Residual diagnosis turns "continue researching" from a vague action into
a clear direction.

== 5.3 Selecting the Descent Direction
<selecting-the-descent-direction>
The next round should not automatically broaden the scope. It should
choose the direction most likely to change the judgment per unit cost.
Three questions can approximate this:

+ Which unknown would most change the action recommendation?
+ Can this unknown be reduced through the next round of desk research?
+ Is the cost of obtaining that evidence lower than its possible
  information value?

If an unknown is important but can only be resolved through future
earnings, real user interviews, field validation, or professional legal
advice, it should not be disguised as a problem that "one more
desk-research round" can solve. The report should mark it as external
validation, future fact, or non-desk research, rather than iterate
forever.

In the Nvidia case, the next direction may not be "continue researching
Nvidia," but a more specific question:

- Are the EPS and exit PE implied by the current price too high?
- Does cloud-provider capital expenditure support continued upward
  revisions over the next two quarters?
- Have in-house chips and alternative suppliers already changed
  long-term gross-margin assumptions?
- If semiconductor exposure is already high, does adding Nvidia improve
  portfolio risk-return?

These questions are closer to descent directions than "continue deep
research."

== 5.4 Update Rules
<update-rules>
Each research round should explicitly state update rules. A simple
format is:

#figure(
  align(center)[#table(
    columns: (50%, 50%),
    align: (auto,auto,),
    table.header([New evidence], [Effect on judgment],),
    table.hline(),
    [Direct evidence supporting the core hypothesis
    strengthens], [Increase the weight of that hypothesis],
    [Opposing evidence strikes the core hypothesis], [Lower confidence
    or pivot],
    [Evidence supports only object quality, not action
    attractiveness], [Keep the "good object" judgment but do not upgrade
    the action recommendation],
    [Evidence shows that a key variable is highly sensitive], [Lower
    conclusion certainty and output a conditional decision],
    [Key evidence remains unobtainable through desk research], [Mark it
    as external validation or future fact],
  )]
  , kind: table
  )

These update rules prevent the agent from "appearing to have read more
material" while the conclusion changes in no explainable way. If new
evidence changes no hypothesis weight, scenario weight, or action
boundary, it is only background information.

== 5.5 Stopping Rules
<stopping-rules>
Iteration should stop only when two conditions are met.

First, the main residuals have been compressed to an acceptable level:
the objective function is clear, constraints are explicit, key claims
have evidence, the strongest opposition has been handled, and sensitive
variables and action boundaries are clear.

Second, the marginal information value of further desk research is
insufficient to change the action recommendation. In other words, even
if one more round is conducted, the most likely new information would
only add details rather than change actions such as buy, wait, avoid, or
continue validation.

Therefore, stopping is not caused by reaching a fixed number of rounds,
nor by having written an attractive conclusion. It is caused by:

- the current conclusion already being sufficiently conditional;
- key counterfactuals having been handled;
- remaining unknowns being correctly classified as future facts,
  external validation, or low-value details;
- the expected information value of continued research being lower than
  the cost.

If these conditions are not met, the final report should not be
generated prematurely.

== 5.6 Iteration Prompt Template
<iteration-prompt-template>
After each round, the following prompt can be used:

Please do not write the final conclusion directly. First perform
residual diagnosis: 1. What is the largest residual in the current
judgment: question, constraint, evidence, hypothesis, adversarial,
sensitivity, or action? 2. Which residual is most likely to change the
final action recommendation? 3. Can the next round of desk research
reduce this residual? 4. If not, should it be classified as a future
fact, external validation, missing user constraint, or professional
responsibility boundary? 5. Please give the smallest next-round
question, rather than saying broadly "continue researching." 6. If the
information value of continued research is already insufficient, explain
why the process can stop and provide the structure of the conditional
final report.

= 6. Residual Metrics and Evaluation Functions in a Discrete State Space
<residual-metrics-and-evaluation-functions-in-a-discrete-state-space>
Chapter 5 discussed how to choose the residual direction. This chapter
defines residuals themselves. Because the state space of open-ended
research is not a continuous Euclidean space, residuals should not be
pretended to be differentiable distances. A better approach is to map
the state into a set of discrete gap levels, then use soft residuals,
hard constraints, and thresholds to define whether the report is "good
enough."

== 6.1 Baseline and Improved Prompts
<baseline-and-improved-prompts>
Baseline prompt:

#quote(block: true)[
Conduct deep research on whether Nvidia's stock is worth buying at the
current stage.
]

Improved prompt:

#quote(block: true)[
Please first reconstruct the objective function, constraints, and key
assumptions of this question, then provide a conditional action
recommendation based on evidence, opposing arguments, valuation-implied
expectations, scenario analysis, and update rules.
]

== 6.2 Residual Component Definitions
<residual-component-definitions>
Given a research state $x$, define the residual mapping:

$ r(x) = (r_q, r_c, r_e, r_h, r_a, r_s, r_j) $

Each component is not a continuous value, but a discrete level. For
execution, one can use:

- $0$: this dimension is sufficient to support the current action
  judgment;
- $1$: this dimension still has a gap, but the gap will not materially
  change the action recommendation;
- $2$: this dimension has a decision-level gap and may change the action
  recommendation;
- $3$: this dimension is seriously missing, and the current report
  should not be finalized.

The mapping is:

#figure(
  align(center)[#table(
    columns: (33.33%, 33.33%, 33.33%),
    align: (auto,auto,auto,),
    table.header([Residual component], [Meaning], [High-residual
      manifestation],),
    table.hline(),
    [$r_q$ question residual], [Whether the original question has been
    reconstructed into the true objective function], [Still answering
    "buy or not," with no defined objective, horizon, or action
    variable],
    [$r_c$ constraint residual], [Whether key constraints are
    explicit], [Missing horizon, budget, position size, risk tolerance,
    responsibility boundary],
    [$r_e$ evidence residual], [Whether core claims have direct
    evidence], [Only broad narratives, no sources, dates, data
    definitions, or conflicting evidence],
    [$r_h$ hypothesis residual], [Whether core hypotheses have been
    tested], [Key growth, competition, valuation, or user-demand
    assumptions remain unverified],
    [$r_a$ adversarial residual], [Whether the strongest opposition has
    been handled], [Risks are only symbolic and cannot falsify the
    current conclusion],
    [$r_s$ sensitivity residual], [Whether variables that would change
    the conclusion are clear], [It is unclear what conditions would move
    the recommendation from buy to wait or avoid],
    [$r_j$ action residual], [Whether the report supports
    action], [After reading, the reader still does not know what to do,
    what to wait for, or when to review],
  )]
  , kind: table
  )

This definition turns "report quality" from a subjective impression into
a set of checkable discrete gaps.

== 6.3 Residual Aggregation Function and Hard Constraints
<residual-aggregation-function-and-hard-constraints>
The total residual can be written as:

$ Phi(x) = sum_i w_i r_i(x) $

where $w_i$ is a weight. Different tasks can use different weights. In
high-risk domains such as investment, medicine, and law, constraint
residual, evidence residual, and adversarial residual should receive
higher weight. In product opportunities and technology selection,
residuals related to user demand, alternatives, execution cost, and
reversibility may matter more. These weighted items are soft residuals:
they allow trade-offs, but they cannot cover up critical gaps.

Hard constraints must also be defined. A hard constraint is not a
"deduction point." It is a pass condition that cannot be compensated for
by other strengths. For example, unclear responsibility boundaries,
complete absence of key evidence, non-executable recommendations, or
writing assumptions as facts may directly block finalization. An
acceptable state can be written as:

$ cal(A) = { x : Phi(x) <= epsilon, max_i r_i(x) <= tau, h_k(x) = 1 " for all " k in K } $

where $cal(A)$ is the acceptable-state set and $h_k\(x\)$ indicates
whether the $k$-th hard constraint is satisfied. The second and third
conditions are both important. Even if the total score looks good, a
report cannot pass if a key dimension has an excessively high residual
or if a hard constraint is not satisfied. For example, a report may
contain abundant evidence and polished writing, but if it does not
address what expectations the current price implies, it may still fail
as an investment decision report.

== 6.4 Evaluation Dimensions
<evaluation-dimensions>
#figure(
  align(center)[#table(
    columns: (33.33%, 33.33%, 33.33%),
    align: (auto,auto,auto,),
    table.header([Dimension], [Low-quality output], [High-quality
      output],),
    table.hline(),
    [Objective function], [Directly answers buy / do-not-buy], [First
    defines return, risk, horizon, position size, and opportunity cost],
    [Fact boundary], [Treats narratives as facts], [Distinguishes facts,
    assumptions, inferences, and value judgments],
    [Evidence quality], [Cites broad materials], [States sources, dates,
    data definitions, and conflicting evidence],
    [Opposing-argument strength], [Risks are mentioned in
    passing], [Gives an opposing logic that can truly falsify the
    conclusion],
    [Sensitivity], [Only one scenario], [Explains how key variables
    change the conclusion],
    [Decision value], [Reads like a material compilation], [Provides
    action boundaries, triggers, and review rules],
    [Updatability], [One-shot conclusion], [States which new evidence
    would change the judgment],
  )]
  , kind: table
  )

This table is the readable version of the residual function. It does not
reward long reports. It identifies which residuals remain uncompressed.

== 6.5 Passing Threshold
<passing-threshold>
A report reaches the passing standard not because it appears
comprehensive, but because it can answer:

+ What is the reader trying to optimize?
+ Which assumptions does the conclusion depend on?
+ Which evidence is strongest, and which is weakest?
+ Which variables are most likely to change the action recommendation?
+ Why is the current action better than alternative actions?
+ If the judgment is wrong, how can the user detect and update it?

If these questions cannot be answered clearly, the report should proceed
to the next research round rather than write a final conclusion early.

In residual language: if any $r_i\(x\)$ remains at a decision-level gap,
the report should continue iterating along that residual direction. Only
when all major residuals are below the threshold and continued research
has insufficient information value to change the action recommendation
should the report enter the acceptable set $cal(A)$.

= 7. Limitations
<limitations>
This method is not omnipotent.

First, it cannot eliminate uncertainty. Constraint optimization and
Bayesian updating can only improve the structure of judgment; they
cannot guarantee correct predictions.

Second, it depends on evidence quality. If sources are stale, data
definitions are wrong, or key data is missing, even a good framework may
produce misleading judgments.

Third, residual measurement itself still requires judgment. The discrete
level of $r_i\(x\)$ is not a number given automatically by nature. It is
an assessment made by the researcher according to task risk, evidence
standards, and action consequences. It is more checkable than pure
subjective impression, but it should not pretend to be a fully objective
physical quantity.

Fourth, weight selection may introduce new bias. The setting of $w_i$
differs across tasks. If the researcher overweights dimensions that are
easy to satisfy, or underweights dimensions that are difficult but
critical, the evaluation function will be distorted. This is also a form
of Goodhart risk: when the quality score becomes the target, the model
may optimize the score rather than the judgment.

Fifth, it may increase research cost. For simple factual questions, the
full process is too heavy. It is more suitable for open-ended decisions
with high uncertainty and high cost. In practice, one should first judge
whether the question deserves full iteration, rather than dragging every
question into a complex process.

Sixth, it cannot replace professional responsibility. High-risk domains
such as investment, medicine, and law still require professional
judgment and clear responsibility boundaries. AI can organize evidence
and reasoning, but should not masquerade as the final responsible party.

Seventh, it can still be corroded by formalism. If an agent mechanically
fills forms and turns each step into an audit checklist, the report will
still lose readability. The real goal is to serve human decision-makers,
not to prove that the agent performed many steps. The value of the
residual framework lies in compressing decision gaps, not in producing
more structured traces.

= 8. Appendix: Reusable Prompt Templates
<appendix-reusable-prompt-templates>
The following templates are not the only correct way to write prompts.
They are a starting point for reconstructing open-ended questions into
decision-optimization problems. The lightweight template fits most
open-ended questions. The full template fits high-cost, high-uncertainty
tasks or tasks requiring multi-round evidence iteration.

== 8.1 Lightweight Template
<lightweight-template>
I want to research an open-ended question:

[fill in the question]

Please treat it as decision research, not as a direct answer to the
surface wording. Output the following six steps:

+ Objective function: what am I really trying to optimize? Is the
  original wording misleading the objective?
+ Constraints: what are the time, budget, risk, resource,
  responsibility-boundary, and opportunity-cost constraints? How do
  missing constraints affect the conclusion?
+ Evidence and assumptions: what are facts, assumptions, inferences, or
  popular narratives? What direct evidence is needed for the most
  important claim?
+ Opposition and sensitive variables: what is the strongest opposing
  argument? Which variable changes would alter the action
  recommendation?
+ Action boundaries: provide conditional recommendations, triggers,
  review rules, and falsification conditions.
+ Residual diagnosis: what is the largest remaining residual? Does the
  next round of desk research have enough information value? If not,
  explain why the process should stop.

== 8.2 Full Template
<full-template>
I want to deeply research an open-ended question:

[fill in the question]

Please treat this as open-ended decision research, not as a direct
answer to the surface wording. Your goal is to help a human
decision-maker form a reviewable, updatable, actionable judgment.

Please output the following process:

#text(weight: "semibold")[I. Objective function]

+ What is the user really trying to optimize?
+ Is this objective consistent with the original wording?
+ If the original wording is misleading, how should it be rewritten?
+ What action must the final report support: choose, rank, enter, exit, buy,
  wait, adopt, abandon, or continue researching?

#text(weight: "semibold")[II. Constraints]

+ What is the time horizon?
+ What is the risk-tolerance boundary?
+ What are the resources, budget, position size, organizational
  capability, or opportunity costs?
+ Which missing constraints would change the conclusion?
+ If constraints are missing, provide conditional judgments under
  different constraints instead of pretending they do not exist.

#text(weight: "semibold")[III. Research framework]

+ What research framework fits this question?
+ What core dimensions does the framework contain?
+ Why does each dimension affect the final action?
+ Which dimensions are only background information, and which dimensions
  truly change the decision?

For securities or company due diligence, consider:
- market environment;
- industry theme;
- business structure;
- financial quality;
- valuation and implied expectations;
- institutional expectations;
- capital flows and technicals;
- catalysts;
- risks and disconfirming evidence.

For product or market research, consider:
- user demand;
- existing alternatives;
- competitive landscape;
- distribution channels;
- willingness to pay;
- unit economics;
- barriers to entry;
- regulatory and platform constraints;
- execution difficulty.

#text(weight: "semibold")[IV. Facts, assumptions, and inferences]

+ What are the known facts?
+ What data requires real-time lookup?
+ What key assumptions have not been verified?
+ Which items are subjective judgments or market narratives?
+ Which conclusions are only inferences and should not be written as
  facts?
+ Which facts, if falsified, would change the final action?

#text(weight: "semibold")[V. Evidence plan]

+ What primary, official, or authoritative sources are needed?
+ Which sources can only serve as auxiliary signals?
+ What evidence must support each key claim?
+ How should source freshness, conflicts of interest, and data-definition
  differences be handled?
+ If evidence conflicts, explain the source of conflict instead of simply
  averaging.

#text(weight: "semibold")[VI. Multi-perspective analysis]

Analyze at least from the perspectives of a supporter, opponent, neutral
analyst, risk manager, and final decision-maker. For each perspective, state:
+ core logic;
+ key evidence;
+ most concerning variable;
+ possible error;
+ impact on the action recommendation.

#text(weight: "semibold")[VII. Counterfactuals and sensitivity]

+ Which key variables most affect the conclusion?
+ If these variables move in the opposite direction, does the conclusion
  change?
+ What evidence would falsify the current judgment?
+ Provide optimistic, base, bearish, and stress scenarios.
+ Explain the action implication under each scenario.

#text(weight: "semibold")[VIII. Implied-expectation reverse-check]

+ What future expectations does the current action imply?
+ What facts must hold for these expectations to be satisfied?
+ To achieve the target return, target growth, or target result, what
  levels must the key variables reach?
+ If the key variables do not reach those levels, what is the loss or
  opportunity cost?

#text(weight: "semibold")[IX. Adversarial validation]

+ Write the strongest supporting argument.
+ Write the strongest opposing argument.
+ Identify the weakest assumption on each side.
+ State which side currently has stronger evidence.
+ Clearly state what evidence is still missing and would change the
  conclusion.

#text(weight: "semibold")[X. Bayesian updating]

+ What is the most likely current explanation?
+ Is current confidence broadly high, medium, or low?
+ What new evidence would raise confidence?
+ What new evidence would lower confidence?
+ What evidence would trigger narrowing the question, pivoting hypotheses,
  abandoning the path, or continuing research?

#text(weight: "semibold")[XI. Integrated judgment and decision tree]

Provide a conditional conclusion, decision tree, next observation metrics,
and review rules:
+ What is the most reasonable current action?
+ Under what conditions can action become more aggressive?
+ Under what conditions should one wait, narrow scope, or abandon the
  path?
+ If the judgment is wrong, how can that be detected?
+ What question is most worth researching in the next round?

#text(weight: "semibold")[XII. Residual metrics]

Use discrete levels from 0 to 3 to evaluate the residuals of the current
report:
+ Question residual: is the report still answering the original wording
  rather than the true objective function?
+ Constraint residual: are time horizon, budget, risk, and
  responsibility boundaries missing?
+ Evidence residual: do core claims have direct evidence?
+ Hypothesis residual: have key assumptions been verified?
+ Adversarial residual: is the strongest opposition strong enough to
  falsify the current conclusion?
+ Sensitivity residual: are the variables that would change the
  conclusion clear?
+ Action residual: does the reader know what to do, what to wait for,
  and when to review?

State the level, reason, and weight for each residual, and whether any
single residual is high enough to block finalization.

#text(weight: "semibold")[XIII. Next-round direction or stopping reason]

If decision-level residuals remain, provide the smallest next-round question,
the needed evidence, expected information value, and cost. If no decision-level
residual remains, explain why the marginal information value of continued
research is insufficient, and provide the conditional conclusion that the final
report should contain.

= 9. Conclusion
<conclusion>
The most dangerous failure mode in open-ended research is not that the
agent fails to find enough material. It is that the agent accepts the
initial direction embedded in the user's question too quickly. It
appears to be helping the user, but may in fact be expanding the user's
initial bias into a structurally complete report. The essence of AI
sycophancy is not flattering tone. It is optimizing the wrong object:
the model treats the user's initial point as the objective function and
treats an apparently complete answer as convergence.

The constraint-optimization perspective proposed in this paper tries to
rewrite this problem into a more robust decision system.
Objective-function reconstruction prevents the surface wording from
misleading the task. Constraint modeling restores the user's real
situation. Multi-start search and counterfactual perturbation prevent
local optima. Adversarial testing and regularization resist popular
narratives. Bayesian updating and decision trees turn conclusions into
revisable, executable action boundaries.

Furthermore, this paper abstracts multi-round research as
residual-driven evidence iteration. Each round is not done to "write one
more round," but to reduce a class of decision residual: question
residual, constraint residual, evidence residual, hypothesis residual,
adversarial residual, sensitivity residual, or action residual. The
discrete residual metric in Chapter 6 provides a checkable evaluation
function for this iteration: when a residual remains at a decision-level
gap, research should continue along that direction; when the main
residuals are below threshold and further research has insufficient
information value to change the action recommendation, the report enters
the acceptable set.

Therefore, reconstructing open-ended research through constraint
optimization is not about adding terminology. It is about changing the
nature of the task:

From: answering what the user asked to: identifying what the user truly
needs to optimize.

From: proving a candidate conclusion to: comparing multiple actionable
options.

From: outputting a one-shot opinion to: building an updatable judgment
system.

From: accumulating more material to: compressing the most important
decision residuals.

For strongly narrated, high-consensus, high-valuation names such as
Nvidia, the core of AI analysis is not to prove that the company is
good. It is to test whether the current price has already fully priced
in that goodness. For any open-ended research task, the core
responsibility of AI is not to accommodate the user's initial wording,
but to help human decision-makers form a clearer, more reviewable, and
more updatable judgment under uncertainty.

This method ultimately serves neither the model itself nor the process
itself, but the human decision-maker. A good research report should not
make the reader see that "the agent did many steps." It should make the
reader more clearly understand what they are truly optimizing, what
current evidence supports, which assumptions are most fragile, what
conditions would change the action, and what next step would lead to
less regret in an uncertain world.

= 10. References and Further Reading
<references-and-further-reading>
+ Sharma, M. et al.~"Towards Understanding Sycophancy in Language
  Models." arXiv:2310.13548.
+ Wei, J. et al.~"Simple synthetic data reduces sycophancy in large
  language models." arXiv:2308.03958.
+ Perez, E. et al.~"Discovering Language Model Behaviors with
  Model-Written Evaluations." arXiv:2212.09251.
+ Ouyang, L. et al.~"Training language models to follow instructions
  with human feedback." arXiv:2203.02155.
+ Bai, Y. et al.~"Constitutional AI: Harmlessness from AI Feedback."
  arXiv:2212.08073.
+ Ben-Tal, A., El Ghaoui, L., and Nemirovski, A. #emph[Robust
  Optimization]. Princeton University Press, 2009.
+ Gorissen, B. L., Yanikoglu, I., and den Hertog, D. "A Practical Guide
  to Robust Optimization." arXiv:1501.02634.
+ Tetlock, P. E., and Gardner, D. #emph[Superforecasting: The Art and
  Science of Prediction]. Crown, 2015.
+ Howard, R. A., and Abbas, A. E. #emph[Foundations of Decision
  Analysis]. Pearson, 2015.
+ Goodhart, C. A. E. "Problems of Monetary Management: The U.K.
  Experience." #emph[Papers in Monetary Economics], Reserve Bank of
  Australia, 1975.
+ Hubbard, D. W. #emph[How to Measure Anything: Finding the Value of
  Intangibles in Business]. Wiley, 2014.
+ Nocedal, J., and Wright, S. J. #emph[Numerical Optimization].
  Springer, 2006.
+ Boyd, S., and Vandenberghe, L. #emph[Convex Optimization]. Cambridge
  University Press, 2004.
+ Powell, W. B. #emph[Approximate Dynamic Programming: Solving the
  Curses of Dimensionality]. Wiley, 2011.
