# Core budget assumptions

This note supports the current [six-month integration plan](INTEGRATION_PILOT.md).
The owner agreed USD 48,000 for the Lead Designer and Internal Controls Specialist,
USD 48,000 for a qualified Software Engineer and USD 4,000 provisional
infrastructure: **USD 100,000 core**, not an all-in final application. It is a
planning model, not authority to hire, buy equipment, activate services,
run CI or call a model/API. Grant allowability is unconfirmed. Public access to
this reviewer repository and its history was approved separately on 19 October
2026, preserving existing licenses and adding no Creative Commons license.

## Engineering capacity examples

The engineering allocation is fixed at **USD 48,000 before employer burden**.
The examples divide it by 26 weeks and the indicated weekly hours:

| Engineer hours/week | Hours over 26 weeks | Illustrative USD/hour |
| ---: | ---: | ---: |
| 40 | 1,040 | 46.153846 |
| 30 | 780 | 61.53846 |
| 20 | 520 | 92.30769 |

Rates are rounded division examples, not offers or market-rate findings. The
eventual agreement must settle hours, rate, responsibilities and scope together.
Fewer engineering hours do not promise the same output; scope, sequencing and
schedule must fit the negotiated capacity. The Lead Designer and Internal
Controls Specialist allocation is USD 8,000/month gross for six months, with a
40-hour paid week. Neither allocation assumes unpaid excess hours.

## Infrastructure allowance example

These are **capacity and spending allowances**, not validated workload
requirements, provider selections or purchase recommendations. Prices were checked
on **19 October 2026**; usage quantities are owner planning assumptions, not
observed consumption or benchmarks. Recheck actual prices, availability,
compatibility and billable extras before any commitment.

| Generic category | Illustrative basis | Six-month USD |
| --- | --- | ---: |
| Local memory hardware | Provisional, unquoted allowance; hardware compatibility, qualified-vendor list (QVL) and actual quote pending. No RAM SKU recommended. | 1,100 |
| Hosting and object storage | Six months at USD 24/month for an example 4 GiB RAM, 2 vCPU, 80 GiB SSD VM plus USD 5/month for 250 GiB object storage: 6 x (24 + 5). [VM pricing](https://www.digitalocean.com/pricing/droplets), [storage pricing](https://www.digitalocean.com/pricing/spaces-object-storage). | 174 |
| Cloud GPU capacity | Example 600 GPU-hours at USD 0.89/hour, using the listed RTX 4090 Pod rate solely as a cost reference: 600 x 0.89. [GPU pricing](https://www.runpod.io/pricing). | 534 |
| GPU network storage | Example 100 GB of standard network storage at USD 0.07/GB/month for six months: 100 x 0.07 x 6. [Storage pricing](https://www.runpod.io/pricing). | 42 |
| CI capacity | Example 30,000 billable minutes at USD 0.006/minute for a Linux 2-core x64 hosted runner: 30,000 x 0.006. [Runner pricing](https://docs.github.com/en/billing/reference/actions-runner-pricing). | 180 |
| API testing | Provisional spending allowance; no provider, model, token volume or validated workload selected. | 1,200 |
| **Illustrative use** | **1,100 + 174 + 534 + 42 + 180 + 1,200** | **3,230** |
| **Unallocated infrastructure headroom** | **4,000 - 3,230** | **770** |
| **Infrastructure category total** | **3,230 + 770** | **4,000** |

The VM/storage quantities and GPU type are examples of purchasable capacity, not
evidence that they fit the application. The quoted GPU example is a Pod rate,
not a serverless inference rate. Standard network storage is a separate allowance;
other attached disks, transfer, backups and service extras may incur additional
charges. The CI example covers the named runner minutes only, not every CI cost;
different operating systems, runner types, storage, job rounding and actual
workloads change costs. This documentation update dispatches no hosted CI.

Existing GPU reuse is an option only if actual compatibility, availability and
testing support it; it is not guaranteed. Free credits, discounts and donated
capacity are not assumed. No hardware requirement, RAM SKU, provider purchase or
performance result has been validated by this budget exercise. Unspent headroom
does not need to be spent and is not an approved transfer to another category.

## Costs and commitments still unresolved

Required employer/payroll costs, benefits, taxes, insurance and administrative
costs have not been quantified or provided for in the core USD 100,000. Hardware
and service taxes, delivery and applicable extras also need actual quotes/terms.
The USD 770 is infrastructure headroom, not a claim that it covers those unknown
costs. Establish a fully costed plan and permitted funding sources before a final
application or engagement.

The owner's willingness to discuss redirecting lead pay does not specify a
reallocation, authorize a pay cut or change the 40-hour lead budget. Any change
needs an explicit revised budget and capacity/scope decision. Optional paid,
supervised student work requires a separate costed plan; it is not an automatic
addition to, or substitution within, the core budget.

The founder reports contributing roughly 50-60 hours/week since October 2025.
That is self-reported prior effort, not verified time records. It has no assigned
historical dollar value in this plan, creates no owed reimbursement and is not
added to the request. Future delivery is planned against budgeted capacity.
