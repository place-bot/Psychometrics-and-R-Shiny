# The Birth of Adaptive Testing and Its Current Status

## Learning Objectives

After studying these notes, you should be able to:

- Explain how adaptive testing originated with Binet's IQ test (1905)
- Identify the 5 key characteristics that differentiate adaptive from conventional tests
- Trace the evolution from Binet to early computer-based approaches
- Analyze why early CAT approaches failed
- Understand the transition to IRT-based CAT

---

## 1. Historical Surprise: Adaptive Testing Came First!

### The Timeline That Challenges Assumptions

| Testing Type | First Implementation | Context |
| --- | --- | --- |
| **Adaptive Testing** | 1905 | Binet's individually administered IQ test |
| **Fixed-Form Testing** | 1918 | WWI military recruit screening |

**Key Insight**: The "traditional" paper-and-pencil test is actually the newer innovation. Adaptive testing is the original approach!

---

## 2. Five Defining Characteristics of Adaptive Testing

According to the text, ANY adaptive test (from Binet to modern CAT) must have these five characteristics:

### Characteristic 1: Calibrated Item Bank

- Items with **known psychometric properties**
- For individual differences measurement: covers wide trait range
- Not just a collection of items - must be pre-analyzed

### Characteristic 2: Variable Starting Point

- Can use **prior information** about examinee
- Different examinees can start at different places
- Contrast: Fixed tests start everyone at Item #1

### Characteristic 3: Flexible Scoring

- Score derived from **different subsets** of items
- Different examinees can get same score from different items
- Items must be on same **predefined scale**

### Characteristic 4: Dynamic Item Selection

- **Predefined rule** for next item selection
- Based on scored responses to previous items
- Real-time adaptation during testing

### Characteristic 5: Variable Termination

- **Prespecified criterion** determines when to stop
- Not fixed number of items for everyone
- Can vary by examinee performance

**Result**: An **individualized test** that is **dynamic** - adjusting difficulty to match examinee trait level during administration.

---

## 3. Binet's Revolutionary Adaptive Test (1905)

### 3.1 The Item Bank Structure

Binet created a sophisticated system:

- **210 total items**
- **21 mental age levels** (5 to 15 years)
- **Half-year intervals** between levels
- **10 items per level**

**Key Concept - Mental Age**:

> "The chronological age of a group of examinees who answered test questions correctly 50% of the time"

Example: If 50% of 10-year-olds answer an item correctly → Mental Age 10 item

### 3.2 The Adaptive Testing Process

**Step 1: Select Starting Level**

- Use prior information if available
- Example: "bright" 8-year-old → start at Mental Age 9
- Default: start at chronological age

**Step 2: Find Basal Level**

- **Basal level** = mental age where child answers ALL items correctly
- Process:
  - Administer items at starting level
  - If not 100% correct → move down
  - Continue until 100% correct achieved

**Step 3: Find Ceiling Level**

- **Ceiling level** = mental age where ALL items answered incorrectly
- Process:
  - Move up from basal level
  - Continue until 0% correct achieved

**Step 4: Calculate Score**

- Mental Age = weighted average of correctly answered items
- IQ = (Mental Age ÷ Chronological Age) × 100

### 3.3 Efficiency Analysis

From the Figure 2-1 example:

| Metric | Value |
| --- | --- |
| Total item bank | 210 items |
| Items administered | 60 items |
| Items skipped (too easy) | 50 items |
| Items skipped (too difficult) | 90 items |
| **Efficiency gain** | **71% reduction** |

### 3.4 Individualization in Action

Different students receive completely different item sets:

| Student | Mental Age Range | Items Target |
| --- | --- | --- |
| A | 7.5 - 10.0 | Average ability range |
| B | 12.5 - 14.5 | High ability range |
| C | 5.0 - 7.0 | Low ability range |
| D | 10.5 - 12.0 | Above average range |

### 3.5 Variable Test Length

Key observations:

- **Student E**: Narrow range → most precise measurement
- **Student F**: Wide range → least precise measurement
- **Insight**: Test provides both score AND precision indicator

### 3.6 Limitations of Binet's Approach

Despite its brilliance, Binet's test had problems:

1. **Cost**: Requires individual administration by psychologist
2. **Partial adaptation**: Must complete all items at a level before branching
3. **No precision control**: Only subjective precision indicator
4. **Limited generalizability**: Age-based metric hard to apply elsewhere

---

## 4. Evolution of Adaptive Testing

### 4.1 Clinical Modifications (1940s-1960s)

Researchers tried to improve Binet's approach:

| Researcher | Year | Innovation | Goal |
| --- | --- | --- | --- |
| Spache | 1942 | Insert easy items after failures | Avoid frustration |
| Hutt | 1947 | Fully adaptive (item-by-item) | Better ending experience |
| Greenwood & Taylor | 1965 | Adaptive WAIS | Clinical efficiency |

**Common theme**: Focus on examinee experience and motivation

### 4.2 The Terminology Zoo

Early adaptive testing went by many names:

- Sequential testing
- Branched testing
- Individualized measurement
- Tailored testing
- Programmed testing
- Response-contingent measurement
- **Adaptive testing** (eventually won)

### 4.3 Theoretical Foundations

Two key theoretical proposals:

1. **Hick (1951)**: Use information theory

   - Harder item after correct response
   - Easier item after incorrect response
   - Target 50% probability of correct
2. **Cronbach (1954/1966)**: Use decision theory

   - Short screening tests
   - Intensive measurement for high scorers
   - Hierarchical abilities model

---

## 5. Early Computer-Based CAT Approaches

### 5.1 Two-Stage Tests

**Structure**:

- **Stage 1**: Routing test (10 items at p = 0.50)
- **Stage 2**: Four measurement tests at different difficulties

**Branching Rules**:

| Routing Score | Branch To | Difficulty (p) |
| --- | --- | --- |
| 0-2 | Least difficult | 0.85 |
| 3-5 | Less difficult | 0.63 |
| 6-8 | More difficult | 0.37 |
| 9-10 | Most difficult | 0.15 |

### 5.2 Multistage Tests (MST)

Extension of two-stage concept:

- Multiple branching points
- Example shows 1-3-4 design
- 120 items in bank, 45 administered per examinee

Note: MSTs are further discussed in Chapter 12.

### 5.3 Pyramidal Structures

#### Constant Step Size

**How it works**:

1. Start with Item 1 (average difficulty)
2. Correct → branch right (harder)
3. Incorrect → branch left (easier)
4. Fixed length (10 items in example)

#### Variable Step Size

**Improvement**:

- Large steps early (quick convergence)
- Small steps late (fine tuning)

### 5.4 The Flexilevel Test

**Unique features**:

- One item per difficulty level
- Paper-and-pencil with self-scoring sheets
- Complex branching rule

**Branching algorithm**:

- Correct → next harder item NOT yet administered
- Incorrect → next easier item NOT yet administered

**Results by ability level**:

- High ability: Items range p = 0.15 to 0.60
- Average ability: Items range p = 0.25 to 0.70
- Low ability: Items range p = 0.40 to 0.85

### 5.5 Stratified-Adaptive (Stradaptive) Test

**Key innovations**:

1. Items grouped into difficulty strata
2. Variable test length
3. Branching after each item
4. Searches for basal and ceiling strata

**Branching rules**:

- Up-one/down-one
- Up-one/down-two
- Others possible


**Key contrasts**:

- Consistent examinee (a): 20 items, narrow range
- Inconsistent examinee (b): 41 items, wide range
- Both achieve ~50% correct overall

---

## 6. Why Early CATs Failed: Critical Analysis

### 6.1 Classical Test Theory (CTT) Limitations

All early CATs relied on CTT, which has fatal flaws for CAT:

| CTT Problem | Impact on CAT |
| --- | --- |
| **Sample-dependent difficulty** | Can't build stable item banks |
| **Ignores discrimination** | Suboptimal item selection |
| **No individual precision** | Can't control measurement error |

### 6.2 Structural Rigidity

Each approach had strict requirements:

| CAT Type | Requirement | Problem |
| --- | --- | --- |
| Pyramidal | Exact difficulty spacing | Hard to find real items |
| Flexilevel | One item per difficulty | Limited item pool |
| Two-stage/MST | Item clusters at difficulties | Somewhat flexible but limiting |
| Stradaptive | Items grouped by difficulty | Most flexible but still constrained |

### 6.3 Scoring Problems

- **Number-correct scores**: Don't account for item difficulty differences
- **Difficulty-based scores**: Ignore item discrimination
- **No error estimates**: Unlike modern Standard Error of Measurement (SEM)

### 6.4 The Flexilevel Paradox

A psychological problem emerges:

```text
After convergence:
Correct answer → Much harder item (feels like punishment)
Incorrect answer → Much easier item (feels like reward)
```

This creates increasingly extreme oscillations!

### 6.5 Fixed vs. Variable Length

| Approach | Length | Problem |
| --- | --- | --- |
| Two-stage | Fixed | Inefficient for some |
| MST | Fixed | Inefficient for some |
| Pyramidal | Fixed | Inefficient for some |
| Flexilevel | Fixed | Inefficient for some |
| Stradaptive | Variable | Better but other issues |

**Key insight**: "Twin objectives of CAT are efficiency and effectiveness" - fixed length violates efficiency.

---

## 7. The IRT Revolution

The text concludes that adaptive testing turned to Item Response Theory (IRT) to solve all these problems. This resulted in CATs that are "highly efficient and effective."

IRT solutions (detailed in Chapter 3):

- Item parameters invariant across populations
- Explicitly models discrimination
- Individual-level precision estimates
- Optimal variable length tests

---

## 8. Current Status: Two CAT Paradigms

Modern CAT primarily serves two measurement problems:

### 8.1 Measurement CAT (Chapter 4)

**Purpose**: Measure individual differences

**Applications**:

- Educational: formative assessment, growth measurement
- Military: ability profiles of recruits
- Health: mental health evaluation, patient-reported outcomes
- Psychology: personality and clinical measurement

### 8.2 Classification CAT (Chapter 5)

**Purpose**: Make decisions or classify into categories

**Applications**:

- Higher education admissions
- Achievement testing in schools
- Certification and licensing
- Human resources hiring and placement

### 8.3 Fully Adaptive CAT

Modern IRT-based CAT characteristics:

1. Calculate θ (trait level) estimate after each item
2. Use θ to select next item from precalibrated bank
3. Continue until termination criterion reached
4. Variable test length (like Binet's original)

Real-world applications are detailed in Chapter 11.

Special CAT types are described in Chapter 12.

---

## Key Takeaways

1. **Adaptive testing is the original approach** - predating fixed tests by 13 years
2. **Five characteristics define all adaptive tests** - from Binet to modern CAT
3. **Binet's test was remarkably sophisticated** - achieving 71% efficiency in 1905
4. **Early CATs were creative but flawed** - limited by CTT and structural constraints
5. **The flexilevel paradox shows psychological considerations matter** - not just psychometrics
6. **IRT solved the fundamental problems** - enabling modern efficient CAT
7. **Two main applications dominate** - measurement vs. classification

---

## Self-Assessment Questions

1. What are the five characteristics that define ANY adaptive test?
2. Calculate the efficiency gain if 75 items are administered from a 300-item bank.
3. Explain why Binet's test required individual administration by a psychologist.
4. What is the flexilevel paradox and why is it psychologically problematic?
5. List three specific CTT limitations that made early CATs fail.
6. Why did the stradaptive test allow variable length while others didn't?
7. What does "fully adaptive CAT" mean in the modern context?

---

Study notes based on Chapter 1 of Weiss & Şahin (2024): Computerized Adaptive Testing: From Concept to Implementation
