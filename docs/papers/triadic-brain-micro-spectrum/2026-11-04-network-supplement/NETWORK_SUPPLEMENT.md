# Triadic Brain network semantics at the representation protocol and execution boundaries

## A source constrained formal treatment of cooperative computation and revisable knowledge

Conceptual and system design: Thomas Prislac, Ultra Verba Lux Mentis

Expanded academic supplement, author-review candidate, 4 November 2026. AI-assisted formal exposition for author review. This document distinguishes existing architecture, inspected implementation, proposed specifications and unresolved obligations. It reports no new product execution, physical-node experiment, confidential-computing qualification or large-network deployment. The frozen technical manuscript edition 1.2 remains unchanged. [P1](#p1)

## Abstract

We formalize Triadic Brain's cooperative network as a collection of independently governed state machines exchanging typed, bounded representations under purpose-specific authority. The treatment separates local authoritative state from remote knowledge of that state; application message identity from transport delivery; resource observation from durable commitment; content integrity from provenance, authorization and epistemic adequacy; and immutable artifact distribution from task-parallel or partitioned inference. A microscopic lifecycle analysis begins with configuration and enrollment, continues through scoped discovery, endpoint selection, framing, canonicalization, authentication, bilateral admission, resource commitment, invocation, capture, result authorization and local interpretation, and ends with replication, correction, revocation, recovery and teardown. Every unclosed join is represented as an explicit proof or implementation obligation rather than filled with an invented successful path. Formal elaborations include typed authority relations, knowledge-state products, admission predicates, crash cuts, typed provenance graphs, correlated-availability models and workload-specific cost estimands. The project-specific account is compared with primary literature on content addressing, remote procedure calls, distributed systems, capability attenuation, attestation and computational provenance. The architectural objective remains practical autonomy and cooperative intelligence, not mere minimization of compute expenditure. Mathematical precision does not establish empirical usefulness, security or scientific novelty; those require separately specified observations and falsifiers. [P1; P2; R-PROV; R-RPC; R-RATS]

## Reading map

Sections 1–7 establish scope, threat models, lifecycle boundaries and cryptographic obligations. Sections 8–16 formalize authority, observer knowledge, resources, effects, storage and provenance. Sections 17–21 operationalize candidate records and transitions. Sections 22–28 analyze scaling and evaluation. Sections 29–31 specify qualification traces, byte witnesses and remaining obligations. Appendix A reconstructs the bounded source protocol, including unjoined interfaces. Proposed specifications and source descriptions are deliberately separate. Equation identifiers F1–F27 belong to the formal model, not to deployed configuration.

## 1 Scope epistemic types and the scientific object

### 1.1 The intended object

The system under study is a federation of locally controlled installations in which a participant can refuse work, preserve local operation, select providers and share only authorized artifacts or resources. Personal, household, organizational and global scopes are separately governed; membership and permissions do not compose transitively across them. The existing design requires no mandatory centrally hosted operational authority, all-to-all adjacency graph, universal scheduler or shared writable custody database. Central software maintenance or authenticated update distribution is compatible with this operational commitment, provided it does not confer access to participants' data or authority to execute their tasks. These are existing project requirements, not conclusions derived from networking literature. [P2, master §17.5.1]

The network carries more than isolated jobs. It carries selected observations, analytical contributions, disagreements, reusable structures, corrections and continuity records. Its cognitive proposition concerns how Sonya/AEGIS admission, UCC context, CoherenceLattice relations, Sophia evaluation, Atlas continuity, PMR retention and TEL provenance cooperate while preserving native meanings. The mathematical models below formalize the communications and authority substrate. They do not replace GUFT with a routing metric, AHA with nearest-neighbor lookup, Sophia with a quorum vote or human judgment with a hash comparison. [P1 §§8–14; P2]

### 1.2 Claim typing

Each substantive assertion belongs to one or more explicitly named classes: **D** denotes an existing design requirement; **S** an inspected source definition; **C** a traced producer-consumer connection; **R** a retained execution report not rerun here; **F** a formal deduction under stated assumptions; **P** a newly proposed elaboration; and **U** an unresolved implementation or observational obligation. The symbols are evidence types, not confidence scores. In particular, S∧C does not entail deployed execution, and F does not entail measured utility. This supplements, rather than silently replaces, the evidence vocabulary of edition 1.2. [P1 §2]

Statements labeled **P** are specifications to evaluate, not assertions that developers have selected a protocol or granted operational permission. The use of requirements language within a proposed profile denotes internal consistency requirements of that profile only. It creates no authorization to install a service, enroll a key, transmit a private object or execute a task. A source-specific limit belongs to its named snapshot; a variable in a model is not an unannounced production default. [P1 §2; P2]

### 1.3 Reproducibility boundary

The public thesis supplies a stable published account and an explanatory machine companion. The present source audit additionally uses a frozen private candidate, with exact file identities retained in a controlled annex. A private citation establishes where the author inspected a fact, but does not grant public reproducibility or independent empirical confirmation. Later code can close a historical join without making that earlier closure retroactively complete. Conversely, an old design requirement is not newly invented because its current implementation is incomplete. [P1 §2; P2]

The scope is microscopic with respect to identified application-level boundaries, not omniscient with respect to every kernel, network interface, model runtime or physical device. For each delegated subsystem the manuscript names the contract, observable behavior and required qualification; it does not claim to have audited every implementation beneath it. Unknown behavior remains U. This limitation is scientifically consequential because an end-to-end safety property depends on the composition of actual consumers, not on the union of individually plausible component descriptions. [P1 §§2, 16; R-E2E]

## 2 System and adversary model

### 2.1 Entities and independently governed namespaces

Let V be the set of participating installations. For node v, distinguish local principals A_v, custody owner C_v, resource owner O_v, gateway G_v, provider adapter P_v and approved key owner K_v where present. These logical roles may share a host but must not be conflated in an authorization proof. Let S be the set of participation scopes, Q the set of tasks, X the set of immutable representations, and U the set of purpose labels. Identifier equality is scoped: the same printable task label at two nodes does not establish the same task, issuer or authority. **P/F:** namespace every remotely meaningful identifier by its authenticated issuing context and protocol/version domain, and define explicit alias-resolution records rather than comparing display names. [P2; R-PROV]

The time-varying communication graph E(t)⊆V×V describes possible directed contacts, not permission or knowledge. Define separate relations Discoverable(v,w,s,t), Reachable(v,w,t), Authenticated(v,w,c,t), Authorized(v,w,q,u,t) and ResultUsable(v,x,q,t). A discovery edge does not entail a reachability edge; a reachable authenticated peer need not be authorized for a task; an authorized task can return an inadequate result. These relation separations are proposed formalizations of existing project boundaries, not five deployed database tables. [P1 §§12–15; P2; R-LIBSEC]

### 2.2 Fault classes

The benign-fault model admits process termination, reboot, disconnection, delay, duplication, partial transfer, queue saturation, resource exhaustion and independently lost acknowledgements. The adversarial model additionally admits malformed messages, dishonest advertisements, replay, identity multiplication, selective omission, routing manipulation, correlated workers, false result assertions, compromised storage replicas and privileged inspection at an ordinary compute endpoint. A compromised local custody owner lies outside guarantees that rely solely on that owner's log. A malicious model can produce a syntactically valid but semantically false answer. Neither case is repaired by content hashing. [P1 §15; R-SYBIL; R-PETALSSEC]

Cryptographic reasoning assumes the selected primitives and implementations meet their declared security goals, trusted reference keys or roots have been established through the chosen enrollment procedure, secrets are not already compromised, and the platform enforces the assumed key boundary. Availability reasoning must not assume the adversary delivers messages merely because integrity is preserved. Privacy reasoning must enumerate timing, size, topology, access-pattern and identifier leakage separately from plaintext exposure. These are assumptions to instantiate and test, not blanket claims of a perfect cryptographic adversary model. [R-TLS; R-AEAD; R-RATS; R-IPFSPRIV]

### 2.3 Safety liveness and knowledge

Safety properties constrain which transitions must never occur: dispatch without current authority; admitting two different byte payloads under one retained idempotency identity; releasing a confidential key to an unbound recipient; or treating a copied artifact as an independent experiment. Liveness properties require eventual progress under explicit conditions, such as eventual reachable owner, available resources and unrevoked permission. An implementation that remains HELD forever can satisfy a narrow nondisclosure safety property while failing its usefulness objective. Report both. [R-LAMPORT; R-RPC; P1 §16]

A timeout is an observation at one node. It does not reveal whether the remote peer never received the request, durably accepted it, invoked a provider, completed work or merely lost the reply. Therefore local uncertainty is an epistemic state, not a remote lifecycle state. The formal transition system must preserve these possible histories until an authoritative reconciliation observation eliminates them. Timeout-induced fresh execution is particularly dangerous when the external effect is not idempotent. This is the project's no-resend requirement expressed in remote-procedure-call terms. [P2; R-RPC]

## 3 Configuration enrollment and discovery before the first task

### 3.1 Local configuration genesis

**D/P:** Before any peer operation, the local owner chooses the supported protocol profile, installation identity, permitted scopes, providers, resource bounds, retention choices and discovery/relay policy. Configuration is a versioned object with an authenticated local acceptance event. Every executable selection resolves to a current protected configuration version, not an arbitrary path or endpoint supplied by a peer. A UI checkbox is an intent producer; the deciding native consumer must verify its current protected realization. A restart must reopen the accepted state through that consumer rather than reconstruct authority from presentation state. [P2; P1 §4]

Configuration changes require a defined transition: previous version, proposed version, authorized actor, effective boundary and affected running operations. A blanket instruction to replace a configuration file is not a proof that in-flight tasks can safely rebind. **P:** distinguish changes applicable only to new tasks, changes requiring cancellation or reconciliation, and emergency revocations that fence future use. Retained records continue to bind the versions under which they were accepted. The serialization of configuration and running-state transitions is an implementation obligation, not supplied by a version number alone. [P2](#p2)

**P/U: software-maintenance authority.** Update publishers, package/configuration signers, dependency suppliers and local installation acceptance are trust roles. Any party able to replace the native policy-enforcement program belongs to its trusted computing base unless a separately protected boundary constrains that replacement. Signed delivery authenticates origin, not benign behavior. Executable versions, rollback and freeze policy must be bound to current authorization and attestation appraisal. Decentralization here means absence of a mandatory online operational controller, not immunity from accepted supply-chain authority. TUF supplies a relevant update-threat taxonomy and metadata comparison; it is not claimed adopted or sufficient to make publisher-authorized code benign. [R-TUF; P2]

### 3.2 Enrollment and pairing

An enrollment procedure establishes which identity or key is accepted for which scope. Possession of a cryptographic key is evidence of key possession, not a unique person, independent operator or authorized organizational representative. **D/P:** record the authenticating channel, owner approval, recipient/purpose scope, supported operations, expiry/freshness policy and revocation generation. Bind a pairing to both sides' accepted context; keep native application credentials distinct from peer credentials. No field copied from a remote request is itself evidence of the corresponding local authorization. [P2; R-SYBIL; R-LIBSEC]

A pairing lifecycle must specify PREPARED, accepted/enabled, superseded and revoked meanings where supported, including what an interrupted update leaves authoritative. The names here are explanatory except where mapped to actual source. **P:** key rotation establishes an authenticated relation between old and new identity material without resetting task history or making an uncertain old operation new. An attacker should not obtain a second execution merely by rotating a pairing, changing a connection or replaying a task under an alternate transport address. Enrollment and rotation procedures require dedicated threat review; no universal trust-on-first-use policy is assumed. [P2; R-LIBSEC]

**P/U: full-snapshot restoration.** A signed epoch, clock high-water value and spent-grant ledger restored together cannot by themselves reveal that they are old. Continuity needs evidence outside that rollback domain, such as a qualified monotonic root, independently retained authoritative checkpoint or mandatory reconciliation with another owner. If none is available, ambiguous restoration must hold old executable authority. The verification trace restores all relevant state, not just one compact head, and identifies the external observation that detects rollback. This is a protocol obligation, not a claim of qualified rollback resistance. [P2; P3]

### 3.3 Advertisement and discovery

**P:** A capability advertisement is an expiring assertion, modeled as Adv=(issuer,scope,protocols,classes,bounds,contact,revision,freshness,signature-or-channel-binding). Its data model must distinguish measured, reported and inferred attributes. A claimed GPU model, free-memory value or model fingerprint is not attested merely because the advertisement is signed. Query responses should be bounded by item count, aggregate bytes, age and deadline. Negative lookup results mean not found within that query's scope and observations, not nonexistence everywhere. [P2; R-KAD; R-LIBSEC]

The project does not currently select a universal overlay. Candidate mechanisms have different semantics: an explicit peer list provides configured contacts; a scoped directory resolves accepted registrations; a DHT performs identifier-based routing; gossip propagates bounded membership or summaries. None substitutes for application admission. Kademlia's XOR metric supports routing under its assumptions; it does not provide Sybil resistance, semantic search or independent failure domains. SWIM is a membership and failure-suspicion comparison, not a grant issuer. [R-KAD; R-SWIM; R-SYBIL]

Discovery privacy is part of the protocol. A public content identifier can reveal interest in a predictable document, and a scoped peer identifier can expose membership through correlation. **P:** declare which fields may leave each scope; distinguish opaque local handles from public identifiers; avoid emitting query text or plaintext-derived identifiers when the data policy disallows them. Encrypting payloads does not automatically conceal routing metadata, advertisement history or access patterns. No general anonymity claim follows from pseudonymous IDs. [R-IPFSPRIV; P1 §15]

### 3.4 Candidate selection and routing

**D:** Prefer an eligible completed result; otherwise consider separately admitted equivalent in-flight work; otherwise select permitted new computation. This is conditional on applicability, rights and task requirements, including any required independent Challenge. A result from the same source family cannot silently discharge a demand for independent evidence. Each candidate has an admissibility vector before any performance score: supported interface, representation/model compatibility, audience, data exposure, current authority, deadline, resource bounds and result contract. [P2; P1 §§12,14]

**P:** Construct an eligible set E_q={v: all mandatory constraints for q hold under current evidence}. A routing score may rank only E_q; a low predicted latency must not compensate for failed confidentiality or rights constraints. Unknown capability can require a separately authorized probe or rejection; it must not be replaced with an optimistic zero cost. Preserve the inputs and version of the routing decision to distinguish a poor estimate from an unauthorized selection. This is constrained scheduling, not a universal scalar of trust. [P2; R-DRF]

### 3.5 Endpoint resolution and connectivity

Endpoint selection binds scheme, host, port, path family and expected identity according to an approved profile. URI syntax alone does not decide whether a target is permitted. **P:** specify redirect behavior, DNS resolution and re-resolution, loopback/link-local/private-address policy, proxy use, environment-variable inheritance and certificate verification. Recheck the actual target after any transformation allowed by the client stack. Reject an unsupported scheme rather than handing it to a generic URL opener. A server-supplied return URL must not become a privileged fetch target without independent validation. [R-URI; R-TLS; P2]

Connectivity may be direct, negotiated through ICE-like candidate checks, relay-assisted hole punching, or an authorized persistent relay path. Each mechanism has its own contact disclosure and resource commitments. A relay can be transport infrastructure without becoming an operational authority, but a deployment whose only usable route passes through one relay has an availability dependency. Record the actual path, not only the intended direct path. Failure to establish one path grants no authority to select a wider audience or unapproved relay. [R-ICE; R-TURN; R-DCUTR; R-RELAY]

## 4 The network stack and representation boundaries

### 4.1 Distinct byte domains

Define at least the following byte domains: B_source for selected source bytes; B_task for application task serialization; B_request for the canonical peer request; B_http for the HTTP body; B_tls for protected transport records; B_result for the canonical returned envelope; B_text for extracted text; and B_artifact for a retained export or manifest. Equality between any two domains requires an explicit transformation identity. A task hash is not a hash of every network packet; an HTTP transcript hash is not a provider response-body hash; base64 is an encoding rather than encryption. The exact multibyte witness in edition 1.2 motivates this separation. [P1 §§3–6]

**P:** For every transformation f: B_i→B_j, record whether it is invertible, lossy, length-changing or policy-dependent and which representation its digest names. Retain separate raw and derived identities when normalization changes bytes. Unicode normalization can make canonically equivalent text share a selected normalized representation, but its form and version are part of that transformation. It must not be silently applied before verifying a signature or a byte-exact reference whose domain is the original text. [R-UNICODE; P1 §5]

### 4.2 Canonicalization and parsers

JSON validity alone is insufficient for stable cryptographic identity. A profile must define object member uniqueness, ordering, strings/escapes, number domains, trailing bytes and maximum depth/count. The project source's own canonicalizer must be analyzed as its own profile; it must not be called JCS merely because it sorts keys. RFC 8785, for example, has specific serialization and property-ordering rules. Deterministic CBOR/COSE is another possible design family, not a retroactive description of the existing JSON wire. [R-JSON; R-JCS; R-CBOR; R-COSE]

**P:** Define Decode_v(b)=x only for an accepted versioned language L_v. Require schema validation before interpreting fields, and require Encode_v(Decode_v(b))=b wherever canonical wire bytes are mandatory. Reject duplicate keys, unsupported critical fields, invalid Unicode, nonfinite numeric values and type confusion under the chosen profile. In languages where Boolean is a numeric subtype, a range check alone may admit a Boolean where an integer is required; exact-type validation belongs in the schema's semantics. These are proposed parser obligations to map against actual code, not claims that every listed rejection already exists. [R-JSON; R-JCS; P1 §3]

The useful differential oracle is not only parser A accepts versus parser B rejects. Compare whether two accepted decodings yield different abstract values, whether two equal abstract values serialize differently, and whether a signed canonical representation is transformed before the deciding consumer sees it. Fuzz nested containers, key collisions, Unicode edge cases, integer boundaries, length discrepancies and extra trailing objects. Bound the fuzz campaign and retain counterexamples, seeds and parser versions. No fuzz execution is reported in this manuscript. [R-JCS; R-CBOR]

### 4.3 Stream framing and partial delivery

TCP provides an ordered byte stream, not application-message boundaries. Application framing must survive a header split across reads, a body split into arbitrary fragments and several messages becoming available in one read. A successful write or transport acknowledgement does not establish application admission or durable commit. These distinctions remain true even if a test fixture happens to deliver a complete JSON object in one callback. [R-TCP; R-RPC]

HTTP framing adds another interpretation layer. **P:** use a maintained parser; bound header size/count and body size; reject ambiguous message lengths according to the supported HTTP profile; prohibit unsupported upgrades/tunnels and automatic redirect or retry behavior for effectful operations. Count bytes before unbounded allocation, distinguish transfer decoding from content decoding, and cap decompressed size and expansion ratio independently. HTTP message length validation is not a replacement for the inner protocol frame bound. [R-HTTP1; R-HTTPSEM]

For a raw frame profile, a candidate fixed-width length prefix must specify byte order, unsigned range, whether the prefix counts itself, allowed zero-length frames and EOF semantics. For an HTTP profile, these fields are governed by HTTP and should not be invented as though present in current code. **P:** state the actual chosen framing mechanism, maximum retained bytes and maximum parse work per message. An incomplete frame at deadline is a retained partial observation or rejection, not a complete request with absent fields defaulted to authority. [R-HTTP1; P1 §12.2]

**P: preauthentication and recovery budgets.** Owner-global ceilings must bound pending sockets, handshake and signature-check concurrency, partial-frame residence, denial logging and aggregate unauthenticated work. Per-peer quotas alone do not bound an unknown or Sybil population. Reserve finite management/reconciliation capacity separately from new-work admission, including bounded audit-event storage; on exhaustion, expose the hold and retain a bounded local recovery path. Do not reclaim capacity by deleting needed deduplication history or repeating an uncertain effect. Qualification must measure both memory bounds and cancellation/reconciliation service under slow-handshake and saturated-ledger attacks. These are candidate requirements, not source-proven liveness. [R-LIBSEC; R-SYBIL; P3]

### 4.4 Channel establishment and replay

TLS authentication verifies the configured peer identity under the selected certificate or key policy; application scope and task authority are checked separately. **P:** pin the supported protocol/version policy, trust-anchor source, hostname semantics, certificate rotation behavior and failure handling. Do not bypass certificate verification to demonstrate connectivity. If TLS early data is enabled anywhere in a stack, its replay properties need explicit treatment before effectful requests are permitted; a secure channel label alone does not supply application-level replay prevention. [R-TLS §§4,8]

Channel identity, pairing identity, local application identity and operation identity form distinct bindings. Reconnection changes transport state, not the previously retained operation. A new connection cannot reset the original deadline, consumption epoch or idempotency record. Conversely, closing a connection does not prove a model process terminated or a reserved resource was released. Protocol teardown requires observations from the owner of each effect. [P2; R-RPC]

## 5 Cryptographic object and key lifecycle

### 5.1 Hashes signatures and authenticated encryption

A digest comparison is meaningful only relative to a trusted expected digest or authenticated manifest root and a declared byte domain. Hash collision resistance is distinct from preimage resistance and from the entropy of the underlying message. Low-entropy private values can be linkable through guessing even when the hash function behaves ideally. **P:** select algorithms and domain separation explicitly; bind protocol version, object class and canonicalization profile so the same octets cannot be misinterpreted as another authorized object type. The cryptographic envelope authenticates a statement; it does not establish that statement's truth. [P1 §13; R-COSE; R-IPFSPRIV]

For a proposed encrypted-object profile, let ciphertext C=AEAD.Enc(K,N,M,A), where K is the data key, N the nonce, M plaintext and A authenticated associated data. The chosen algorithm's nonce requirements are mandatory. A generic promise to use encryption does not specify nonce allocation, persistence across crashes, key reuse, tag length, associated-data binding or authentication-failure behavior. **P:** bind object class, version, intended scope and immutable manifest context in A as appropriate to the selected scheme; do not decrypt or expose unauthenticated plaintext before acceptance. This is a candidate design, not an implemented crypto suite. [R-AEAD](#r-aead)

If keys are derived, the KDF profile must specify input key material, salt assumptions, context labels and output length. Task/recipient/object separation belongs in the derivation context or independently scoped keys, not in an undocumented naming convention. HKDF is a relevant standardized extract-and-expand construction, but its citation does not establish the source or entropy of a deployment's master material. Role credentials, pairing tokens and object-encryption keys remain distinct secrets with different purposes. [R-HKDF; P2]

### 5.2 Key ownership and release

The existing wallet-like design concerns protected key custody and narrowly authorized release. It does not require currency, a blockchain or a public audit trail of private activity. Enrollment, permitted recipients, task/output scope, rotation, recovery and revocation belong to the key owner's authenticated policy. A browser or peer request must not select an arbitrary key-service endpoint, trust anchor, secret path or callback. **U:** no general confidential-release implementation or hardware qualification is established by this document. [P2, confidential-release plan]

The proposed protected-release chain is: approved guest generates receiving key; fresh evidence binds that public key to the expected workload and execution boundary; verifier appraises evidence under an explicit policy; relying key owner independently authorizes the exact task/recipient/resource version; owner conditionally consumes a one-use attempt; protected material is encrypted to the bound key; outcome is retained and reconciled under the same attempt if acknowledgement is lost. Each arrow is a separate proof obligation. Attestation evidence is not itself an authorization grant, and a valid public-key field does not establish exclusive private-key custody. [P2; R-RATS; R-KMS]

**P/U: possession and channel binding.** The release protocol must establish possession of the private receiving key inside the approved boundary and bind that possession to the appraised evidence, exact attempt, intended recipient and current session or equivalent authenticated context. A copied attestation document or substituted public key must not redirect release. Freshness, trust-chain validation, measurement appraisal and key possession are separate obligations. No particular proof-of-possession exchange is selected or implemented here. [R-RATS; R-KMS]

**P/U: retransmission boundary.** A lost release acknowledgement must not create a new key-release attempt. If retransmission is permitted, it must replay only the previously committed ciphertext or receipt to the same authorized recipient under the same attempt, after current policy checks; it must not silently repeat an irreversible key-use effect. Whether a key service supports this distinction remains an integration obligation. [P2; R-RPC]

### 5.3 Cross owner revocation and uncertainty

Reading current native policy and then performing an unrelated key-service release introduces a time-of-check/time-of-use interval. **P:** define a serialized owner-side conditional-consume protocol with durable epochs and a revocation acknowledgement whose meaning is explicit. A revocation completed before the release linearization point must win under that protocol; a later revocation cannot recall disclosed plaintext. Native SQLite and a remote key service are not one atomic transaction. RFC 9334 defines architectural roles and appraisal relationships, not this cross-owner transaction protocol. [P2; R-RATS; R-LINEAR]

Offline operation exposes a deliberate tradeoff: a worker with a previously issued, unexpired authorization may be unable to learn a new revocation. The policy must choose an admissible freshness window, online check or fail-closed hold; it cannot simultaneously claim instantaneous global revocation and unrestricted disconnected availability. Expiry bounds permission only under its actual clock/freshness assumptions. Replaying an old signed grant after a crash is not safe merely because its signature verifies. [P2; R-MACAROONS]

### 5.4 Plaintext and metadata exit analysis

Authenticated additional data (AAD) is integrity-protected but not encrypted by the AEAD construction; task identifiers, policy references and other sensitive metadata must therefore not be placed there under an assumption of confidentiality. The release-binding tuple must identify the release service, request/input digest, receiving key, workload and configuration, appraisal-policy version, resource/key epoch, output policy and attempt; the profile assigns a trusted verifier to each field. Key persistence, guest cloning/snapshot recovery and post-release output routing remain explicit U obligations. [R-AEAD; R-RATS; R-KMS]

A confidential route must enumerate outputs, provider capture, logs, traces, swap, snapshots, crash dumps, device buffers and human-visible interfaces. CPU attestation does not qualify an attached accelerator. A privileged ordinary worker may inspect inputs and memory; an ordinary container or virtual machine does not establish confidentiality from its host administrator. Specialized MPC or FHE mechanisms require their own supported computation and threat model and cannot be inferred from distributed storage. No secret or plaintext should be introduced into provenance merely to make an audit record complete. [P1 §15; R-RATS; R-PETALSSEC]

**P:** classify each retained field by content sensitivity, linkability, owner, audience, retention, deletion capability and legal/organizational hold. Separate operational evidence needed for private qualification from a public derivative. Public reporting must not reveal credentials, private endpoints, organizational membership, identifying prompts or linkable hashes by default. A raw-free artifact can still contain normalized source or answer text; omission of one raw buffer is not anonymization. [P1 §15]

## 6 Interpreting received work without erasing its origin

**P: output-authority containment.** Remote model text, retrieved evidence, provenance descriptions and rendered artifacts remain data, including when they contain imperative instructions. Indirect prompt injection demonstrates why textual inclusion must not confer tool or policy authority. The proposed interpreter parses the expected schema, preserves origin labels, applies context-specific output escaping, forbids automatic execution of embedded commands or links, and requires a separate owner-authorized operation for every tool effect. A valid digest, approved peer or successful review does not authorize instructions inside the content. Test malicious text at each retrieval, summarization, critique, synthesis and rendering boundary; do not describe prompt wording alone as a complete defense. This is a proposed containment boundary, not evidence that every current consumer enforces it. [R-INJECTION; P2]

### 6.1 Source provenance and local assessment

Model a retained contribution as at least three distinct entities: the producer's claim about its work, the receiver's observation of delivery, and the receiver's current assessment/use decision. A message can truthfully be recorded as received while its producer's execution claim remains unverified. A local Synthesis that cites the contribution is a new activity, not a retrospective local execution of the remote Challenge. W3C PROV's entities, activities, agents and derivations provide a vocabulary for this distinction; conformance requires a concrete mapping, not merely a citation. [R-PROV; P1 §§12–14]

The result acceptance predicate must factor syntax, byte identity, authenticated origin, bound lineage, current rights, method applicability and evidence adequacy. A classifier that outputs one PASS field without preserving these axes invites category errors. **P:** retain a typed acceptance vector and an explicitly scoped decision function rather than treating one successful predicate as a universal endorsement. The decision function is local and versioned; another node can reach a different justified assessment without altering the original bytes. [P1 §13.2; P2]

### 6.2 Dependence and epistemic diversity

Distinct endpoint identities do not prove independent evidence. Workers can share model weights, training data, prompts, source documents or the first worker's answer. Copies of one artifact are one production lineage with several receipt/use lineages. A repeated evaluation may be useful, but its inferential interpretation depends on what was independently varied or observed. **P:** record evidence-family and exposure relationships when available; preserve UNKNOWN when they cannot be established. Do not use a count of agreeing nodes as an empirical estimate of correctness without a calibrated dependence model. [P1 §12.1; R-DEBATE]

The intended Analyst→Challenge→Synthesis decomposition therefore targets distinct functions and exposed assumptions, not an automatic majority-vote theorem. A Challenge can improve the process by identifying a missing premise even if no new answer is generated. Synthesis must preserve material disagreement and unresolved questions. The network's role is to transport and bind these contributions, not to replace scientific adjudication with communication success. [P1 §§10–12]

### 6.3 Reference grammar and correction propagation

An abbreviated reference is usable only after resolving its versioned definition, dependencies, domain, units, permitted uses and residuals. The cost of distributing and maintaining that shared grammar belongs in the communication and reuse budget. A short code transmitted over a fast network does not prove lossless semantic compression. Existing GUFT/AHA structures can make relations inspectable, while target applicability remains a separate empirical question. [P1 §§8–11,14]

**P:** represent corrective information as a new event relating a new interpretation to an earlier object, preserving both identities and the scope of correction. Distinguish retracting a claim, revoking a use grant, marking bytes unavailable, replacing a method and discovering an alternative support path. These transitions have different consequences. A generalized dependency-aware reopening engine, minimal repair-set solver and cross-node revocation propagation remain separate implementation obligations; a dependency graph alone does not execute them. [P1 §14.2; R-PROV]

### 6.4 Scientific innovation without premature novelty claims

The architectural opportunity lies in a composition: scoped resource cooperation, accountable artifact reuse, explicit epistemic dependence, typed cross-domain relations and locally revisable governance. The components have established predecessors, while the particular composition and proposed cognitive use must be evaluated on their own merits. This manuscript makes no priority claim that the composition is unprecedented. **P:** an innovation candidate is a falsifiable change to an identified mechanism with a comparator, resource envelope, rights boundary, adverse cases and rollback condition. A new name, formal symbol or network topology is not itself such evidence. [P1 §§1,16; P2]

### 6.5 Cognitive interfaces preserved across the network

**D/S/P:** The network is a substrate for existing inquiry functions, not a replacement cognitive architecture. The following crosswalk carries their established distinctions into proposed network contracts. It neither asserts that every named component runs in every profile nor turns an existing component into a new wire service. A profile must resolve the actual producer and deciding consumer for each carried field. [P1 §§4,7–15; P2]

| Existing inquiry function | What a network contribution must preserve | What the network must not infer |
|---|---|---|
| Sonya/AEGIS admission and UCC context | Exact accepted task, context and effective control-profile bindings; whether a particular check was executed, advisory, unavailable or merely defined | A remote role label or copied policy identifier is local admission. P1's inspected observation profile does not run every UCC policy as an executable veto. |
| CoherenceLattice relations and GUFT/AHA structures | Native quantity namespace, producer/version, domain and units; mapped relations, source references, disanalogies, residuals and declared target falsifier where supplied | Similar coordinates establish a transferable relation; a structurally reviewable AHA case establishes observed target utility; a network lookup implements automatic analogical discovery. |
| Sophia evaluation and Atlas continuity/orientation | The exact assessed artifacts, checks actually performed, limitations, unresolved findings and required human continuation | A valid transport receipt is a passed audit; a passed audit is an action grant; HOLD means the received text is necessarily false or useless. |
| PMR retention and TEL/custody provenance | Separate retention choice, content-bearing custody obligations, local event order and producing versus receiving/using activities | No optional PMR write means no content was stored; TEL sequence labels measure elapsed time; copying a record creates another original experiment. |
| The existing discovery spiral | A bounded unresolved question, candidate relations, targeted observations, preserved dissent and a new revision's dependencies | An unresolved condition autonomously authorizes more calls; more outputs or greater agreement demonstrate innovation. |

The last row preserves the existing corridor, tributary, river, braiding, terrace and reopening vocabulary as inquiry functions. A network can carry a corridor's question, a tributary's observation or a revised support structure without identifying those functions with packets, routing paths or physical fluid flow. Each new exploration remains bounded by its own source, recipient, resource and action permissions. [P1 §10.1; P2]

## 7 Lifecycle boundary inventory

The inventory below is a proposed completeness checklist for the stated application protocol scope. Each row needs a deciding owner, typed input/output, durable state where relevant, failure observation and acceptance evidence. A row marked U cannot be removed because an adjacent stage passes. The inventory is not a claim that all rows are implemented or tested. [P1 §16; P2]

| Boundary | Required microscopic question | Minimum retained discriminator |
|---|---|---|
| Installation | Which exact executable/configuration is selected and who may change it? | Version and accepted configuration binding |
| Local identity | Which authenticated principal initiates the task? | Native principal/version, not payload role text |
| Pairing | Which peer and operations did both sides accept? | Current scoped pairing and revocation state |
| Advertisement | Which fields are measured versus reported? | Issuer, freshness, supported schema and bounds |
| Discovery | What scope and budget bounded the search? | Query scope, expiry, response size and omission meaning |
| Candidate choice | Why is this peer eligible for these data and task? | Constraint evaluation before performance ranking |
| Endpoint resolution | Which actual address/path was contacted? | Resolved endpoint and approved redirect/proxy policy |
| NAT and relay | Which path carries bytes and who learns metadata? | Actual direct/relay path and permitted disclosure |
| Channel handshake | What identity and protection were verified? | Supported channel profile and failure reason |
| Local intent | What exact operation was authorized? | Original operation identity and exact payload binding |
| Serialization | Which canonical byte language is used? | Schema/version, encoder, decoder and byte digest |
| Framing | What bounds apply before allocation/parsing? | Header/body/expansion limits and partial-transfer status |
| Peer authentication | Which current peer identity reaches native custody? | Protected credential/pairing check |
| Native authentication | Which local actor is allowed to publish the request? | Native actor identity distinct from peer token |
| Admission | What current policy and scope are checked? | Exact grant/configuration/request binding |
| Duplicate handling | Is this the same retained operation or conflicting payload? | Owner-scoped idempotency lookup and conflict result |
| Queueing | Which deadline and capacity constraints still apply? | Original deadline and current state |
| Resource commitment | Who actually owns and enforces CPU/GPU/RAM? | Durable owner reservation or explicit HOLD |
| Dispatch | Which single attempt is released to the provider? | Transactional claim and effect boundary |
| Provider request | What exact model/runtime/input reaches the endpoint? | Provider profile and actual transmitted representation |
| Worker execution | What bounds are enforced rather than advertised? | Observed lifecycle and enforcement evidence |
| Capture | Which raw and extracted bytes were retained? | Separate lengths/digests and completion observations |
| Result construction | Which record produced the envelope? | Same-record binding and declared result contract |
| Result disclosure | Is this exact output currently releasable? | Current disclosure authorization, not merely job expiry |
| Result transport | What was actually received before deadline? | Complete/partial/rejected/unknown observation |
| Verification | Which predicates passed and which remain unknown? | Typed integrity/authenticity/lineage/permission vector |
| Interpretation | Which claims are adequately supported for this task? | Method/version, support, dissent and uncertainty |
| Local synthesis | Was a new local operation separately authorized? | New local task with exact external contribution lineage |
| Provenance commit | Which owner committed which event and ordering? | Durable local event identity and cross-node references |
| Replication | Which new owner may retain which representation? | Recipient, retention, rights and exact manifest |
| Availability repair | May another replica be created under current rights? | Failure observation and authorized repair scope |
| Correction | Which earlier use or claim is affected and why? | Immutable correction relation and present-use decision |
| Cancellation | What future progression is stopped at each owner? | Acknowledged owner-specific cancellation meaning |
| Revocation | Which future authorization is denied and when effective? | Durable epoch/current-state observation |
| Recovery | Which uncertain attempt is being reconciled? | Same identity and authoritative outcome, no blind resend |
| Retention expiry | Which exact copies are removed or remain? | Content-bearing inventory and truthful tombstones |
| Teardown | Which sockets/processes/reservations are actually closed? | Owner-observed closure, unreleased uncertainty retained |
| Departure | Can the participant leave and retain permitted local function? | Export, provider choice and no mandatory network dependency |
| Public reporting | Which facts can safely leave the qualification record? | Separately approved sanitized derivative |

The inventory distinguishes a *negative observation* from a *negative outcome*. Failure to observe a grant, result or closure cannot be converted to proof that the corresponding remote event did not happen. Likewise, a validated byte sequence does not imply successful implementation of every row that could have produced it. These distinctions motivate the formal protocol and evaluation sections that follow. [R-RPC; P1 §§2,13]

## 8 Domains and assumptions

Let \(V\) be the set of administrative nodes, \(\mathcal P\) the set of principals, \(\mathcal S\) the set of sharing scopes, \(\mathcal O\) the set of immutable representations, and \(\mathcal A\) the set of permitted operation types. A node is an enforcement boundary controlled by an owner; one physical machine can host several boundaries, and one administrative node can contain several processes. A principal is an identity accepted by an enforcement boundary. A pseudonymous peer key, a local application identity, a human owner and an external model-provider account need not be the same principal. Let \(\operatorname{owner}(v)\) identify the authority responsible for node \(v\), without assuming that every node has a different owner.

A concrete request is the typed tuple

\[
q=(\nu,\iota,a,p,r,s,\alpha,I,\theta,L,\mathcal D,\tau),
\tag{F1}
\]

where \(\nu\) is the protocol/profile version; \(\iota\) is an operation identifier; \(a\) is the authenticated initiating actor; \(p\) is the stated purpose; \(r\) is the exact recipient or resource owner; \(s\) is the scope; \(\alpha\in\mathcal A\) is the requested operation; \(I\) is an ordered collection of typed input references; \(\theta\) describes the workload and compatibility requirements; \(L\) contains the declared limits; \(\mathcal D\) is the permitted output/disclosure policy; and \(\tau\) is the timing contract. The recipient's local application principal is obtained from its trusted local invocation context, not from \(a\) or any sender-controlled field.

This tuple is a semantic model. A wire format must additionally define field presence, maximum sizes, accepted encodings, unknown-field handling, error behavior, cryptographic algorithms and algorithm-version transitions. A field named “purpose” makes the purpose explicit for enforcement and audit; it does not prove that a malicious recipient actually uses the data only for that purpose.

The baseline network model permits message loss, duplication, reordering, finite but unbounded delay, partitions, process crashes and recovery. A stronger deployment profile may add timing bounds. Safety claims must identify which components are assumed to enforce their rules correctly. Local authorization has no guarantee against an already-compromised enforcement process unless another specified mechanism constrains that process. Cryptographic identities assume uncompromised signing keys and the security of the selected algorithms. Durability assumes stated storage behavior, not that a successful in-memory write survives a crash. Distinct peer identifiers do not imply distinct people, owners, machines, power supplies, networks, software defects or adversaries.

These assumptions should be carried beside each proposition. There is no single fault model under which every property in this supplement follows.

## 9 A multiplex graph with explicit authority

### 9.1 Physical reachability and permitted action

Represent the network as several time-dependent directed relations rather than one graph whose edges ambiguously mean “connected”:

\[
G^{\mathrm{link}}_t=(V,E^{\mathrm{link}}_t),\quad
G^{\mathrm{disc}}_{s,t}=(V,E^{\mathrm{disc}}_{s,t}),\quad
G^{\mathrm{store}}_{s,t},\quad G^{\mathrm{exec}}_{s,t}.
\tag{F2}
\]

The first relation describes usable transport paths under a declared connectivity profile. The second describes permission to exchange discovery metadata in scope \(s\). The latter relations describe candidate storage and execution relationships. An edge in one relation does not generate an edge in another. In particular, there is generally no implication

\[
(u,v)\in E^{\mathrm{link}}_t
\Longrightarrow
\operatorname{Permit}_v(q,t).
\tag{F3}
\]

Likewise, a path \(u\to v\to w\) does not authorize \(v\) to reveal \(u\)'s data to \(w\). A routing path can include a relay authorized to carry encrypted bytes without authorizing it to read their plaintext. The recipient, relay and storage audiences therefore belong in separate policy predicates.

For an enforcing owner \(v\), let \(\pi_v^e\) be the owner's policy at durable local revision \(e\), \(\gamma\) a presented grant, and \(z_v\) the current local enforcement state. A candidate authorization decision is

\[
\operatorname{Permit}_v(q;\pi_v^e,\gamma,z_v)
=\operatorname{Authn}_v(a)
\land\operatorname{RecipientMatch}_v(r)
\land\operatorname{GrantValid}_v(\gamma,q,\pi_v^e)
\land\operatorname{PolicyAllows}_v(q,\pi_v^e)
\land\operatorname{ContextAllows}_v(q,z_v).
\tag{F4}
\]

Authentication, policy and grant evaluation are separate checks. A cryptographically valid grant from an issuer that the recipient does not trust for the stated scope contributes no authority. The grant need not encode all policy. An owner can impose additional current restrictions even when an old signed grant has not expired.

For a disclosure or effect involving several independent owners, the relevant admission condition is the conjunction of the applicable owners' permissions, not their union. A requester may authorize disclosure of its own inputs but cannot allocate another participant's GPU. A worker may consent to GPU use but cannot confer rights to an organization's records. The exact set of owners whose permissions are required is itself a policy decision and must be explicit.

### 9.2 Scopes and attenuation

Let \(\llbracket\gamma\rrbracket\) denote the set of request contexts admitted by a grant, including actor, object, purpose, recipient, operation and time conditions. A delegated grant \(\gamma'\) is attenuated when

\[
\llbracket\gamma'\rrbracket\subseteq\llbracket\gamma\rrbracket
\tag{F5}
\]

and the parent grant permits delegation by that issuer. This formulation avoids assuming that all scopes form one hierarchy. “Household,” “research team” and “public” can overlap in membership without one inheriting another's data rights. Membership in both scopes is insufficient for cross-scope export.

Set inclusion alone does not enforce cumulative limits. If a grant permits at most \(b\) bytes of total disclosure, issuing two child grants each bounded by \(b\) can overspend the parent budget. A candidate budget model allocates child budgets with

\[
\sum_j b_j+b_{\mathrm{owner}}\le b,
\tag{F6}
\]

or charges all uses against one serialized parent counter. Here every term is measured in bytes for a byte budget; distinct units require distinct counters. The same issue occurs for job counts, token limits and monetary ceilings. Independent offline consumers cannot share a strict unpartitioned budget without an additional coordination or trusted-enforcement mechanism. Allocated sub-budgets permit disconnected operation at the cost of stranded capacity and a separate protocol for reclaiming it.

Derived objects require explicit policy propagation. If an output \(o\) incorporates inputs \(I\), a conservative candidate requires

\[
\operatorname{DisclosureAllowed}(o,d,p)
\Longrightarrow
\bigwedge_{x\in I_{\mathrm{relevant}}}
\operatorname{DerivationPolicy}_x(o,d,p),
\tag{F7}
\]

where \(I_{\mathrm{relevant}}\) records the inputs that affected the output under a stated derivation rule. If the relevant-input subset cannot be established by a sound, declared derivation analysis, a conservative implementation includes every admitted input whose information could influence the output; absence from an incomplete provenance record does not exempt an input. An authorized release or declassification can supply a separate exception. A summary is not automatically nonsensitive; a role name, shortened answer or changed file format does not prove that protected information has been removed. This is an enforcement requirement, not a claim that unrestricted natural-language outputs can be completely analyzed for all information leakage.

### 9.3 Local serial order and the revocation boundary

Every consequential owner-controlled step needs a named decision point. Let \(\operatorname{Lin}_v(x)\) denote the position of operation \(x\) in an owner's durable linearization order, preserving real-time precedence of completed operations. For a one-use release, a candidate atomic owner transaction performs: read the current policy revision, validate the exact request, check the unconsumed record, mark that record consumed, and bind the release result to the operation identifier. Let \(g\) identify an immutable owner-scoped grant instance and \(k\) be the full operation key defined in (F11). Let \(z^-\) and \(z^+\) denote the protected pre-state and post-state of one transaction. The candidate commit predicate consistently binds grant, operation, request and policy epoch:

\[
\operatorname{ReleaseCommit}_v(g,k,q,e)
\Longrightarrow
\operatorname{Permit}_v(q;\pi_v^e,\gamma,z^-)
\land\operatorname{Consumed}_v(g,z^-)=\bot
\land\operatorname{Consumed}_v(g,z^+)=k.
\tag{F8}
\]

In addition, the cumulative accepted history must contain at most one committed release effect for each owner-scoped grant instance g. Operation deduplication and grant consumption are different invariants: two different k values cannot consume the same one-use g. An identical retry may retrieve an existing receipt or committed ciphertext only under the profile's current disclosure policy, without another release effect. This counter limits the named owner release, not every subsequent use of a disclosed key or every model invocation. Merely checking policy and later calling a different secret-release service does not establish atomicity. A separate materializing owner needs its own serialization and reconciliation contract.

Let \(r_g\) revoke grant instance g, and let \(x_{g,k,q,e}\) be a proposed release attempt for the same instance. Then

\[
\operatorname{Lin}_v(r_g)<\operatorname{Lin}_v(x_{g,k,q,e})
\Longrightarrow\neg\operatorname{ReleaseCommit}_v(g,k,q,e).
\tag{F9}
\]

A release ordered before revocation can remain historically valid even when later use or redisclosure is forbidden. An owner must not silently rewrite that earlier release as nonexistent. A revocation known only to one disconnected node cannot instantly constrain a different node that continues using cached authority. A profile must choose online checking, bounded-lived authority with declared clock assumptions, or a stated period of stale authorization. This is a scope-and-connectivity limitation; it is not a proof that all decentralized authorization is impossible.

Local serial order is compatible with decentralization. It requires each owner to order its own sensitive effects. It does not require one global mutable authority or a network-wide ledger.

## 10 Representation identity and bounded parsing

### 10.1 Four identities that must not be conflated

A request can have at least four distinct identities: the caller's operation identifier \(\iota\); the hash of the exact received frame bytes; the hash of its validated canonical semantic representation; and the hash of an associated input artifact. Compression, encryption and normalization can introduce further byte representations. Define each digest with an explicit domain tag and unambiguous encoding:

\[
h_{\mathrm{req}}=H(\operatorname{enc}(\text{request-domain},\nu,\operatorname{canon}_{\nu}(q))),
\qquad
h_{\mathrm{wire}}=H(\operatorname{enc}(\text{wire-domain},\nu,B_{\mathrm{wire}})).
\tag{F10}
\]

Here \(\operatorname{enc}\) is an injective encoding for the allowed typed values, implemented with explicit lengths or another specified framing discipline. String concatenation without delimiters is not an adequate definition: \((\text{ab},\text{c})\) and \((\text{a},\text{bc})\) otherwise become indistinguishable. Digests are identifiers under cryptographic assumptions, not mathematical proofs that collision is impossible.

For an unadopted comparison, if JSON Canonicalization Scheme is selected, the profile must actually follow its input and serialization requirements. RFC 8785 excludes duplicate properties, uses a specified number representation and preserves Unicode string data without normalization. It is an Informational RFC, not a claim that arbitrary JSON parsers already agree. [RFC 8785, §§3.1–3.2](https://www.rfc-editor.org/rfc/rfc8785.html#section-3.1)

Application-level normalization remains a separate transformation. Normalizing a transcript or replacing line endings can be useful, but its output receives its own identity and provenance edge. An invalid signature cannot be rescued by changing the signed data into a more convenient representation.

### 10.2 Idempotency binding

Let

\[
k=(\text{recipient-owner},\text{authenticated-actor},\text{scope},\iota)
\tag{F11}
\]

be a deduplication key. The authoritative record binds \(k\) to \(h_{\mathrm{req}}\), the original timing contract, admitted policy revision and outcome references. A repeated \(k\) with the same bound request denotes the same attempt; a repeated \(k\) with different bound bytes is a conflict. A new transport connection, session or return address does not create a new execution permission or reset the original deadline.

This semantics requires a retention rule. If the owner deletes all deduplication state while an old request can still be replayed, the same key may become executable again. A bounded protocol must either retain a tombstone for the replay horizon, reject expired request epochs before deduplication, or define a durable nonreusable key namespace. An infinite exactly-once guarantee cannot be inferred from a finite cache with an undocumented eviction policy.

### 10.3 Parsing and verification as a bounded operation

Bounds apply before the attacker-controlled input causes the allocation or work. A receiver needs separate limits on wire length, decoded length, nesting depth, string size, collection count, proof length, algorithm identifiers and decompression work. A claimed length is checked against both the contract ceiling and actual received bytes. Hash verification does not remove parser risk; malformed bytes can already exhaust resources before they are hashed or semantically rejected.

A candidate admission sequence is: establish a bounded frame; validate structural encoding; resolve the supported protocol profile; validate canonical representation and field types; authenticate the relevant binding; evaluate scope and current policy; allocate bounded resources; then dispatch. Some profiles may authenticate a fixed header before accepting a body. The security argument must describe that actual order and its maximum untrusted work, rather than imply that “signed JSON” alone is safe.

## 11 Protocol state and knowledge of state

### 11.1 A product state instead of one success flag

For an operation \(q\), define its candidate distributed state space as a product

\[
\mathcal S_q=
\Sigma_{\mathrm{auth}}\times
\Sigma_{\mathrm{resource}}\times
\Sigma_{\mathrm{execution}}\times
\Sigma_{\mathrm{receipt}}\times
\Sigma_{\mathrm{use}}.
\tag{F12}
\]

A state \(\sigma_q(t)\) lies in a reachable subset \(\operatorname{Reach}_q\subseteq\mathcal S_q\); not every syntactic coordinate combination is legal. Receipt and use coordinates may themselves be products over recipients. These coordinates answer different questions. Authorization records which permission was valid at each decision point. Resource state records reservations, physical occupancy and release evidence. Execution state records what the authoritative executor or provider actually did. Receipt state records what each recipient obtained and verified. Use state records whether that recipient currently accepts the result for the specified inquiry. Each coordinate has an owner; no participant is assumed to read the complete product.

Examples of reachable combinations include: authorized and reserved but never dispatched; dispatched and completed but no reply received; bytes received with a valid digest but no current disclosure permission; authorized output received but semantically inadequate; and a previously accepted result later superseded by a correction. These combinations make a single Boolean “success” inadequate for recovery, accounting and scientific interpretation.

Owner journal states also differ from physical provider effects. A journal entry “dispatch intent persisted” establishes an intention. A provider receipt “accepted” establishes an attributable statement under the provider contract. Neither automatically proves that the model began computing or that the intended GPU held an exclusive reservation.

### 11.2 Observer uncertainty

Let \(h_i\) be the local observation history of participant \(i\), and let \(\Omega(h_i)\) be the set of system executions consistent with that history and the declared fault model. Fix a historical cut c in each pointed execution; for a fact \(F_c\) about that cut, define the observer's possible-value set

\[
K_i(F_c\mid h_i)=\{F_c(\omega):\omega\in\Omega(h_i)\}.
\tag{F13}
\]

For the historical predicate \(F_c=\operatorname{ExecutedBefore}(q,c)\), a timed-out sender may have

\[
K_i(F_c\mid h_i)=\{0,1\}.
\tag{F14}
\]

One compatible execution lost the request before dispatch. Another executed it and lost the reply. A timeout alone cannot remove the second execution from \(\Omega(h_i)\). The sender can accurately record “no result observed by the local deadline,” but cannot derive “the remote effect did not occur.”

Authenticated reconciliation can reduce uncertainty if the reconciled owner and its durable record are trusted for the relevant fact. A dishonest owner can sign a false assertion; authenticity alone does not shrink the physical-state possibilities to truthful states. The profile must distinguish evidence of the owner's assertion from evidence of independently observed execution.

For instantaneous state, the set of possible values evolves as unobserved execution continues. For already-completed historical events, reliable new observations can exclude previously possible histories. This distinction avoids treating every status poll as a fresh permission or pretending that an old observation remains a current resource reservation.

### 11.3 Causal order and real-time deadlines

Events can be ordered locally and through message send/receive dependencies. Let \(\to\) be the transitive closure of those relations. A logical clock can satisfy \(a\to b\Rightarrow L(a)<L(b)\), while the converse generally fails. Thus, sorting all events by a logical timestamp creates a useful consistent order but does not prove that one unrelated event caused another or establish elapsed wall time. [Lamport 1978](https://lamport.azurewebsites.net/pubs/time-clocks.pdf)

A timing contract must say which clock determines expiry. For a duration \(\Delta\) measured by one owner's monotonic clock, the owner can enforce \(m_{\mathrm{now}}-m_{\mathrm{start}}\le\Delta\) without trusting another node's wall clock. To enforce an absolute external deadline \(D\), suppose the local clock estimate \(c_v(t)\) has a verified error bound \(\epsilon_v\) in the same time unit. The conservative acceptance check

\[
c_v(t)+\epsilon_v<D
\tag{F15}
\]

is sufficient to establish \(t<D\) under that bound. Without a usable bound, the stronger statement is unsupported. Clock rollback, suspended machines and restoration from snapshots must be addressed by the chosen monotonic/durable timing mechanism.

Duration authorization and completion prediction must also be separated. Permission to begin before \(D\) does not imply permission to continue after \(D\), nor prove completion before \(D\). The request profile must distinguish a latest-start time, execution cutoff, disclosure cutoff and result-use expiry when those differ.

## 12 Task graphs and owner admitted placement

### 12.1 Tasks as typed dependency vertices

Let an inquiry revision be a finite directed acyclic graph

\[
\mathcal T=(J,F),
\tag{F16}
\]

where each vertex \(j\in J\) is one bounded activity and each edge \((u,j)\in F\) identifies a required input or control dependency. An edge carries the expected artifact type, identity or admissible identity relation, completeness requirement and use policy. The graph is acyclic within one revision. An iterative Challenge/Synthesis cycle is represented by new vertices \((j,r+1)\) depending on prior-revision outputs, not by silently overwriting an earlier vertex or creating a self-justifying evidence cycle.

For candidate worker \(v\), define

\[
\operatorname{Ready}(j,v,t)=
\bigwedge_{u\in\operatorname{pred}(j)}
\left[
\operatorname{Available}(o_u,v,t)
\land\operatorname{Verified}(o_u,v)
\land\operatorname{Applicable}(o_u,j)
\land\operatorname{UsePermitted}(o_u,j,v,t)
\right].
\tag{F17}
\]

Readiness is therefore more than the completion of predecessors. A complete predecessor may have produced the wrong model version, an inadmissible partial result, a revoked data release or an output that the next worker is not permitted to see. Conversely, a declared task may permit a particular partial result or an explicit missing-input branch. That choice belongs to its contract rather than a scheduler's undocumented improvisation.

### 12.2 Feasible placement

For an indivisible task, let \(x_{jv}\in\{0,1\}\) indicate proposed placement at \(v\). Before admission,

\[
\sum_{v\in V}x_{jv}\le1,
\qquad
x_{jv}\le\operatorname{Eligible}(j,v,t).
\tag{F18}
\]

The inequality permits holding a task with no qualified worker. \(\operatorname{Eligible}\) is a conjunction of current scope permissions, technical compatibility, recipient confidentiality qualification if required, owner participation and local admission feasibility. It is not a scalar reputation score. No amount of predicted speed makes an ineligible placement permissible.

Equation (F18) is a planning constraint, not a distributed mutual-exclusion mechanism. Two independent schedulers could each satisfy their own local copy while issuing conflicting assignments. A task owner therefore retains the authoritative assignment identity and reconciles it at the effect boundary. Intentional duplicate computation is represented as separately authorized replica activities with distinct identifiers and an explicit duplicate-execution policy. It is never inferred from a timeout.

For partitioned inference, the vertices must represent actual executable partitions with activation formats, model and tokenizer identities, execution semantics and transfer edges. Summing RAM advertised by disconnected peers does not create a feasible placement for an indivisible model. A feasibility proof must bind each partition to memory local to its executing boundary and each dependency to a permitted, usable data path.

### 12.3 Resource dimensions and commitment

Let \(\mathcal R\) contain explicitly typed resource dimensions, for example CPU cores, host RAM bytes, accelerator RAM bytes, persistent storage bytes, simultaneous provider calls and egress bytes per second. For worker \(v\), \(C_{vr}(t)\) is enforceable capacity for dimension \(r\), \(b_{vr}(t)\) is an owner-protected reserve, and \(R_{jvr}(t)\) is the resource commitment attributed to activity \(j\). A conservative admission condition is

\[
\sum_{j\in\mathcal C_v(t)}R_{jvr}(t)
\le C_{vr}(t)-b_{vr}(t)
\quad\text{for every }r\in\mathcal R,
\tag{F19}
\]

where \(\mathcal C_v(t)\) includes obligations not yet safely released. All terms in one inequality have the same unit. CPU seconds are a work budget and cannot be added to a core-count capacity. Bandwidth rates require a simultaneous-usage or reservation interval model; a total-byte quota is a separate dimension. Accelerator compute rate depends on precision, kernel, device and workload, so a bare “GPU unit” is not a universal capacity measure.

An uncontrolled capacity decrease may invalidate the commitment inequality without a new admission. The owner must expose the deficit and stop new admissions, not erase unresolved commitments to make accounting appear feasible. Controlled capacity reductions wait for qualified release or an authorized enforced transition; physical failure is not assumed preventable.

An advertisement \(\widehat C_{vr}(t_0)\) is not \(C_{vr}(t)\). A scheduler may use the advertisement to find candidates, but the actual owner must atomically update its own admitted obligations before promising scarce capacity. If two requests read the same free-memory value and both reserve it without serialization, each can look feasible individually while their sum violates (F19).

Physical enforcement is a separate obligation. If actual consumption \(U_{jvr}(t)\) can exceed \(R_{jvr}(t)\), then (F19) bounds accounting entries rather than real usage. A memory limit, scheduler quota, isolated device allocation or provider-side concurrency limit can supply a relevant enforcement mechanism, but each must be qualified for the actual resource and failure mode. A request exceeding its bound must be stopped, throttled or moved into a declared breach state. Calling an estimate a “reservation” does not supply any of these mechanisms.

### 12.4 Uncertain duration and unresolved occupancy

When durations and demand are random, a forecast may use the conditional chance constraint

\[
\Pr\!\left[
\exists t\in[t_0,t_1],r:
\sum_j U_{jvr}(t)>C_{vr}(t)-b_{vr}(t)
\;\middle|\;\mathcal F_{t_0}
\right]\le\alpha,
\tag{F20}
\]

where \(\mathcal F_{t_0}\) is the available evidence and \(\alpha\) is a declared overload-risk tolerance. This is meaningful only with a justified joint model for demand and capacity. Multiplying independent-job probabilities is invalid when jobs share model caches, devices, host memory, workload bursts or failures. A collection of per-task quantiles is not automatically a bound on the probability of any overload across the full horizon. Equation (F20) is a forecasting goal, not a hard safety guarantee.

For safety under uncertain completion, define \(\mathcal C_v(t)\) to retain every accepted obligation not released by authoritative evidence or by an independently enforced end to its occupancy. Loss of a reply is not release evidence. An expired scheduler lease might allow a new coordinator to act while the old provider job continues; releasing both the lease and its resource accounting immediately can oversubscribe the same device. A bounded lease safely releases resources only when its expiration is coupled to actual resource revocation or a mechanism that prevents old work from consuming the protected capacity.

There are consequently two different availability outcomes: an owner may preserve safety by holding an uncertain reservation, and it may lose usable capacity while reconciliation is unavailable. That is a measurable operational cost. Inventing a new attempt to improve apparent throughput merely hides the unresolved obligation.

## 13 Effect boundaries and exactly once claims

### 13.1 A minimal indistinguishability argument

Consider a non-idempotent external effect \(E(q)\) performed by a provider outside the receiver's local transaction. After sending the request, the receiver crashes before recording a definitive result. Two executions can leave the same durable receiver state:

1. The provider never received the request and no effect occurred.
2. The provider performed the effect and its reply was lost before the receiver recorded it.

On recovery, resubmission can cause a duplicate in the second execution; refusing resubmission can leave the first execution incomplete. Local logging alone cannot distinguish them. The ambiguity is removed only by an additional justified mechanism, such as a provider-owned durable idempotency record, a queryable operation identity with adequate semantics, or a transaction protocol covering the relevant effect. Some providers offer none. The correct outcome then remains uncertain rather than being promoted to exactly once.

The original RPC literature already makes the distinction between a returned result and a failure report whose execution outcome is uncertain. Birrell and Nelson's particular implementation specifies one invocation when the call returns and leaves callers uncertain between zero and one invocation after an exception. This is a precedent for carefully bounded semantics, not a guarantee inherited by this project. [Birrell and Nelson 1984, §3.1](https://www.cl.cam.ac.uk/teaching/0708/DigiCommI/birrell1984rpc.pdf)

### 13.2 Scope of an exactly once statement

Let \(N_E(k)\) count committed instances of a named externally observable effect for deduplication key \(k\). At-most-once effect safety means

\[
\forall\omega\in\Omega:\quad N_E(k,\omega)\le1.
\tag{F21}
\]

A corresponding liveness statement requires that \(N_E(k)=1\) eventually under specified assumptions: the request remains authorized, required owners recover, resources remain feasible, communication eventually works and the effect service satisfies its contract. Exactly-once effect semantics combines these properties within that boundary. It is not the same as receiving exactly one network message, invoking a process exactly once, producing one retained object, returning one answer, or billing once. A system can repeat harmless internal work while committing one effect, or invoke a worker once while that worker performs several effects.

Even for deterministic computation, duplicate execution can consume additional energy, scarce resources, provider quota or money. Semantic equality of two outputs does not make their operational effects identical. A reproducibility claim also requires the actual source, parameters, model/runtime versions and relevant nondeterminism assumptions, not merely a shared task label.

### 13.3 Fencing and what it does not provide

Suppose an authoritative resource epoch \(f\) increases whenever ownership changes. An effect sink retains the highest accepted epoch \(f_{\max}\), validates that the epoch was legitimately issued for the correct resource, and rejects operations with \(f<f_{\max}\). It must update the stored epoch and apply the protected write in a suitable atomic operation. This protects against a delayed old owner only once the sink knows the newer epoch or otherwise checks current authority. A client-side assertion that its lease is valid cannot substitute for sink enforcement.

The Chubby paper gives a concrete precedent in which a lock sequencer is passed to the affected server and checked there. The relevant lesson is the location of the check, not a requirement to adopt Chubby or a global lock service. [Burrows 2006, §2.4](https://www.usenix.org/legacy/event/osdi06/tech/full_papers/burrows/burrows.pdf)

Fencing alone does not suppress two deliveries with the same current epoch. Idempotency binding is still needed. Nor can a new epoch undo plaintext already disclosed or cancel a provider operation that does not honor that epoch. If a sink checks only the largest epoch it has observed, a delayed old operation can still arrive before the first new-epoch operation. Claims about revocation from a particular moment require a stronger current-authority check or an explicit ordering argument.

### 13.4 Cancellation and reconciliation

Cancellation is a request to prevent specified future progression. A useful contract distinguishes “cancellation requested,” “execution cutoff enforced,” “resource released,” “result disclosure forbidden” and “historical outcome reconciled.” A cancellation acknowledgement must state which of these it establishes. The absence of further output is not evidence that a provider stopped computing.

Reconciliation queries the same operation identity at the owner whose state can resolve the uncertainty. It may reveal “not admitted,” “admitted but not dispatched,” “running,” “completed with result binding,” or “outcome unavailable.” Those responses have different retry implications. “Not found” permits resubmission only if the owner's record-retention and admission contract makes it authoritative evidence of nonexecution for the original request epoch. A forgotten or inaccessible record is not such evidence.

### 13.5 Consensus limits in their exact domain

FLP concerns deterministic consensus among at least two fully asynchronous message-passing processes. Even with reliable eventual message delivery to nonfaulty processes and at most one crash failure, agreement and nontriviality cannot be combined with guaranteed decision in every admissible run. It is an existence result about a nondeciding execution, not a claim that consensus usually fails, that all distributed systems require a central controller, or that timeout-based RPC uncertainty is itself the FLP theorem. [Fischer, Lynch and Paterson 1985](https://groups.csail.mit.edu/tds/papers/Lynch/jacm85.pdf)

A deployment claiming liveness for replicated owner state must state what supplements this model, such as eventual timing bounds, a suitable failure detector or randomized termination semantics. Partial synchrony is one established alternative model. [Dwork, Lynch and Stockmeyer, primary technical report](https://dspace.mit.edu/entities/publication/108bf327-aff6-414b-a48f-b357a821c48e)

Triadic cooperation need not solve a single global consensus problem for every inquiry. Independently governed nodes can retain different judgments while exchanging attributable evidence. Where they do require one answer, such as which operation consumed a one-use grant, the specification must identify the exact participants, consistency property, failure assumptions and availability tradeoff. Agreement on a ledger entry does not establish the scientific truth of the entry's content.

## 14 Immutable objects and Merkle integrity

### 14.1 A concrete candidate identity construction

All budgets and resource amounts in this model are nonnegative; counts are integers, and denominators representing capacities are strictly positive. Let \(B\) be one finite byte string of length \(n\), and let a declared chunking algorithm produce the ordered list \((b_0,\ldots,b_{k-1})\) with \(B=b_0\Vert\cdots\Vert b_{k-1}\) and \(\sum_i|b_i|=n\). For this candidate, n=0 uses k=0 and the empty-tree root; n>0 uses k≥1 and nonempty chunks. Chunking occurs in a specified identity domain: plaintext, encoded plaintext or ciphertext. The manifest states which. Define a raw chunk identifier and a leaf record by

\[
c_i=H(\operatorname{enc}(\text{chunk-domain},\nu,|b_i|,b_i)),
\qquad
e_i=\operatorname{enc}(i,|b_i|,c_i).
\tag{F22}
\]

The index prevents a proof of one position from silently authorizing a different position; the length prevents ambiguous reconstruction. A tree function can use disjoint leaf and internal-node tags:

\[
T([])=H(\operatorname{enc}(\text{empty-tree},\nu)),\quad
T([e])=H(\operatorname{enc}(\text{leaf},\nu,e)),
\tag{F23}
\]

and for a list of length \(k>1\),

\[
T(e_0,\ldots,e_{k-1})=
H(\operatorname{enc}(\text{node},\nu,
T(e_0,\ldots,e_{m-1}),T(e_m,\ldots,e_{k-1}))),
\tag{F24}
\]

where \(m\) is the largest power of two strictly smaller than \(k\). This defines a unique tree shape for every positive length. A deployed specification would assign exact byte tags and widths; the notation here is not itself a wire encoding.

RFC 9162 specifies an ordered Merkle construction with separate leaf and internal-node hashing and explicit inclusion verification. It is a useful primary reference for these design requirements. Its certificate-log application and trust model are not imported by using a similar tree. [RFC 9162, §2.1](https://www.rfc-editor.org/rfc/rfc9162.html#section-2.1)

Define a manifest

\[
M=(\nu,\text{hash-profile},\text{chunk-profile},\text{codec},
n,k,r_T, h_B,\text{encryption-profile},\text{policy-reference}),
\tag{F25}
\]

where \(r_T=T(e_0,\ldots,e_{k-1})\) and \(h_B=H(\operatorname{enc}(\text{object-domain},\nu,n,B))\). The manifest's canonical bytes receive a distinct digest, and an optional detached signature binds those bytes to an authenticated issuer. Signature bytes do not recursively belong to the signed object's own identity unless the envelope construction explicitly resolves that dependency. Likewise, ciphertext construction must not circularly require a final ciphertext root as authenticated associated data used to produce that same ciphertext. A concrete encryption profile must identify a noncircular authenticated header and the fields bound at each stage.

### 14.2 What an inclusion proof establishes

An inclusion verifier takes the authenticated manifest-bound expected root, tree size \(k\), index \(i\), leaf data and a bounded list of sibling hashes. It checks \(0\le i<k\), derives directions from the specified tree shape, rejects missing or extra proof elements, and recomputes the root. For this tree, an individual proof has at most \(\lceil\log_2 k\rceil\) sibling hashes for \(k\ge1\). If the hash output is \(h\) bytes, the sibling-hash portion is at most \(h\lceil\log_2 k\rceil\) bytes, excluding index, size, headers and the leaf. This is a size bound for this construction, not a measured network cost or a bound for every Merkle scheme.

A successful proof shows consistency of that leaf with the expected root under the encoding and hash assumptions. The expected root must itself be obtained through an authenticated or explicitly trusted reference. An attacker who substitutes both data and an unauthenticated root passes a purely local recomputation. Inclusion does not prove who created the content, that it was truthful, that the other chunks remain available, that a peer retained a copy for the promised period, or that the recipient may use it.

Reconstruction checks all required indices and lengths, concatenates in the declared order, verifies \(n\) and \(h_B\), then performs decoding and domain validation within independent bounds. An erasure-coded object requires a different manifest containing the code, coding parameters, encoded shard identities and the original-object binding. “Any \(m\) of \(n\)” is valid only for the chosen code and correct, distinct shards; the statement does not survive arbitrary corrupt shards without verification or an additional error-correction model.

### 14.3 Storage promises and retrieval events

A signed storage receipt is an attributable promise at a time. It is not continuous proof of possession or future availability. Define a commitment

\[
\kappa=(\text{owner},\text{object/shards},\text{retention interval},
\text{retrieval audience},\text{quota},\text{repair rights},\text{evidence policy}).
\tag{F26}
\]

A successful retrieval is a separate event: the authorized requester obtains a reconstructible object that verifies before a declared deadline. Availability probabilities therefore refer to a requester, path, object, deadline and authorization state, not merely whether a host is powered on. Replica placement and repair are meaningful only when \(\kappa\) permits the resulting audience and retention.

Independent-replica calculations require independent retrieval-success events, which can fail because replicas share hardware, cloud accounts, network paths, keys, software or policy authorities. No additional replica repairs a common missing decryption key. This draft leaves quantitative availability and correlated-failure estimation to the supplement's performance section; the integrity model above defines a deadline-qualified retrieval event. The later point-in-time replica model uses a different event and does not by itself establish successful retrieval before a deadline; a timing model is needed to connect them.

### 14.4 Integrity and confidentiality domains

Plaintext and ciphertext digests expose different information. Publicly exposing a plaintext hash of a predictable object can permit offline guessing. Randomized encryption can prevent simple ciphertext equality matching while reducing cross-object deduplication; exact leakage depends on the full design. Key release, chunk discovery, access logs and object sizes can reveal additional metadata even if payload encryption holds.

A hash-valid ciphertext must still pass the encryption scheme's authentication and decryption checks before plaintext is used. Decryption permission can expire even while ciphertext remains available. Revocation can prevent a future enforcing owner from releasing a key, but it cannot make a recipient forget plaintext or a key already obtained. The integrity model does not establish confidential computation at an ordinary worker.

### 14.5 A bounded retrieval and retention lifecycle

The candidate object lifecycle separates locating an object, acquiring bytes, verifying them, committing a retained object and later disclosing it. Each step has its own possible failure and authority boundary. The following sequence is a specification candidate; it does not presume that a particular repository already implements these transitions.

**Authorize the lookup.** The requesting node first checks permission to query the chosen discovery or storage audience for the particular representation. Even a query containing only a digest can disclose that the requester is interested in an object. The storage owner separately checks whether the authenticated requester may retrieve the manifest or chunks. Manifest-read, ciphertext-read, key-release, plaintext-use and redistribution rights are not collapsed into one “download” permission. If public object lookup is deliberately allowed, the applicable policy states that choice explicitly.

**Authenticate and bound the manifest.** Before following attacker-selected locators, the requester validates the expected manifest identity or signature, protocol version, recognized algorithms, sizes, integer ranges, chunk count, tree size and permitted object type. A profile supplies finite ceilings \(n_{\max}\) for reconstructed bytes, \(k_{\max}\) for chunks, \(b_{\max}\) for each transferred chunk, \(m_{\max}\) for encoded manifest bytes and \(p_{\max}\) for each proof. Length accumulation is checked for overflow and must satisfy \(\sum_i|b_i|=n\le n_{\max}\). Merely having \(|b_i|\le b_{\max}\) does not bound the total when \(k\) is unbounded. The encoded proof length is bounded independently of whether its claimed tree size is plausible.

**Select permitted sources.** A retrieval plan assigns required indices or shards to eligible owners and records a finite query budget, concurrent-transfer limit and deadline. A peer advertisement is a candidate source, not verified possession. A missing source may be replaced only by another source within the already authorized audience and the same representation contract. Switching from an encrypted object to a publicly discoverable plaintext variant is not a harmless location change. A privacy-preserving plan must consider the metadata exposed to each source and any relay, not only the final plaintext recipient.

**Stage partial data.** A transfer writes into a quarantined staging namespace associated with \((h_M,\iota)\), where \(h_M\) is the admitted manifest identity. A bitmap or equivalent bounded structure records which exact indices have verified. Before reserving storage, the receiver charges both expected incoming bytes and staging overhead against a local quota. It enforces per-transfer, per-peer and aggregate staging ceilings; otherwise many individually bounded incomplete transfers can exhaust the host. A repeated chunk can update receipt evidence without allocating another unbounded copy. Resume is permitted only against the same admitted manifest and remains subject to current retrieval permission and the original applicable deadline.

**Verify before promotion.** Each staged chunk must match its length, identifier and inclusion position. Unverified chunks remain ineligible for ordinary object consumers. When all required data is available, reconstruction verifies the original object binding and bounded decoding rules. If the manifest identifies ciphertext, this stage establishes ciphertext integrity; plaintext is separately obtained only through an authorized decryption path. A complete object can then move to a committed namespace through an atomic or recoverably journaled transition that binds its index entry to the verified representation. Crash recovery must not leave an index saying “complete” while the required bytes were never durably committed. A chunk streaming consumer is allowed only under a separate contract that says which partially verified prefixes it may act upon and how later failure affects its outputs.

**Record custody and disclose separately.** The owner records the retained object, verification profile, retention promise and source receipts. A transfer acknowledgement can distinguish “bytes received,” “chunks verified,” and “object durably committed.” It must not advertise the third merely because the first occurred. Committing the object does not authorize returning it to every future requester. Each later disclosure undergoes its own present-use and audience checks, including any key-release restrictions.

**Replicate and repair.** Replication creates a new custody obligation at a specifically authorized recipient. Repair can restore a missing permitted replica or reconstruct a missing shard, but neither missing data nor a target replica count authorizes expanding the audience. Before repair, the initiating owner checks current redistribution rights, destination eligibility, retention terms and resource budgets; the new owner performs its own admission. A repair record identifies which verified representation and shard indices were copied and how the replacement was verified. If the only surviving copies are unreachable, unauthorized or lack usable keys, the correct repair state remains blocked or uncertain rather than “healthy” on the strength of an old replica receipt.

**Evict under retention policy.** A disposable cache entry and a promised retained replica are different obligations. Cache eviction can be allowed immediately under its contract; a retention commitment cannot be silently satisfied by deleting its bytes and preserving the receipt. If an owner fails or must terminate a commitment, it records a retention failure and, when permitted, an observable notification or replacement transition. Deleting a local chunk may also affect several locally deduplicated manifests, so eviction checks their live references and outstanding commitments. Reference counting is an accounting mechanism that itself needs crash-safe updates; a counter is not proof that all remote consumers no longer need an object.

**Retain bounded negative history.** A tombstone can record that an object version, storage promise, grant or request identity is no longer admitted and can prevent stale advertisements or old requests from reactivating it. The tombstone retention horizon must cover the corresponding replay and advertisement lifetimes, or the namespace must supply an alternative durable epoch rule. A manifest hash can remain a linkable private identifier, so a tombstone need not be public and should retain only required metadata. A local deletion record attests to the owner's action under its storage mechanism; it is not proof that another recipient erased plaintext or that every underlying medium was sanitized.

These stages have distinct metrics. Partial transfer completion is not full reconstructibility; full reconstructibility is not a successful authorized retrieval by deadline; and retrieval today is not fulfillment of tomorrow's retention obligation. Erasure coding can change the reconstruction condition and storage overhead but does not remove shared failures, malicious shard returns, missing keys, repair bandwidth or current dissemination restrictions.

## 15 Provenance and the difference between replication and evidence

### 15.1 Typed provenance

Let \(\mathcal G_P\) contain entity vertices for immutable representations, activity vertices for transformations and agent vertices for attributable responsibility. Edges include “used,” “generated,” “derived from,” “associated with” and “attributed to.” W3C PROV supplies a standard conceptual vocabulary for these relations and explicitly distinguishes the entities, activities and agents involved. It does not itself certify the truth or completeness of a submitted provenance record. [PROV-DM](https://www.w3.org/TR/prov-dm/)

For a retained contribution, the useful minimum is an output entity, a producing activity identifier, exact admitted input bindings, workload identity, relevant policy/permission references, the producing owner's attributable receipt, and later verification/use activities. A transfer creates a custody or receipt activity referring to the existing output. It does not create another original execution. A normalizer creates a new derived entity even when its intended textual meaning is unchanged.

Provenance assertions have their own authorship and evidence. A worker's statement that it used a particular model can be retained as that worker's assertion; it must not silently become a locally observed fact. Missing provenance is recorded as missing. Different pseudonyms or different output filenames do not establish independent executions.

### 15.2 Claim support and source dependence

Let \(C\) be a claim and \(E_1,\ldots,E_m\) its candidate evidence records. An edge \(E_i\rightsquigarrow C\) records a proposed support relation under a named appraisal rule. Such an edge is not a permission grant, and it is not made true by signing it. Support, challenge, qualification and supersession should be represented distinctly. A local acceptance event records the rule, the evidence available to that local evaluator and the permitted present use.

For a binary hypothesis \(Y\), probability calculus illustrates why copied support cannot be counted as fresh independent evidence. When the relevant conditional probabilities are defined and nonzero, posterior odds obey the chain-rule identity

\[
\frac{\Pr(Y=1\mid E_1,\ldots,E_m)}{\Pr(Y=0\mid E_1,\ldots,E_m)}
=
\frac{\Pr(Y=1)}{\Pr(Y=0)}
\prod_{i=1}^{m}
\frac{\Pr(E_i\mid Y=1,E_{<i})}
{\Pr(E_i\mid Y=0,E_{<i})}.
\tag{F27}
\]

Here \(E_{<i}\) denotes the observed events or values \((E_1,\ldots,E_{i-1})\). Replacing those factors by \(\Pr(E_i\mid Y=1)/\Pr(E_i\mid Y=0)\) requires conditional independence given each hypothesis. Separate machines do not supply that assumption. If \(E_2\) is a deterministic copy of already observed \(E_1\) and the copy channel adds no information about \(Y\), the conditional factor contributed by the observed copy is one. Replication can improve access to evidence without increasing evidence for the claim in this model.

This is an explanatory probability identity, not a proposal to assign numerical posteriors to every GUFT or AHA relation. The needed likelihoods are often unavailable. The operational consequence is simpler: retain common-source, shared-model, shared-prompt, prior-answer-exposure and common-owner dependencies so that an evaluator does not mistake the number of returned artifacts for independent corroboration.

Three distinct claims require distinct evidence: independent execution means the computation actually occurred separately; independent observation means the underlying information was acquired separately; independent error behavior is a statistical property relative to a stated task distribution. None follows from role names such as Analysis, Challenge and Synthesis. A Challenge shown the first answer may be valuable because it critiques that answer, even though the resulting contribution is intentionally dependent on it.

### 15.3 Revision without historical erasure

A correction creates a new entity and a relation to the earlier claim or artifact. It can invalidate a future use while leaving the earlier bytes, receipt and decision history unchanged. Define \(\operatorname{Accept}_i(C,u,e)\) as evaluator \(i\)'s acceptance of claim \(C\) for use \(u\) under appraisal revision \(e\). A later \(\neg\operatorname{Accept}_i(C,u,e+1)\) does not imply the original record was forged or that all other evaluators have already changed their position.

This permits revisable common structures without pretending there is one instantaneous global knowledge state. It also creates a distribution obligation: the system must say how permitted consumers discover corrections and what freshness is required for a later use. A node offline from the correction source can retain useful local work while honestly reporting that its view is not known to be current.

## 16 Candidate invariants and discriminating traces

The preceding models can be summarized as proof obligations for a concrete implementation. The notation \(\Box P\) means that property \(P\) holds at every state of an execution admitted by the chosen fault model. It is a specification target here, not a model-checking result.

**Authority at effect.** For every owner-controlled release or dispatch, \(\Box(\operatorname{EffectCommit}(q)\Rightarrow\operatorname{PermitAtCommit}(q))\). Historical validity and current validity are recorded separately. If policy and effect live at different owners, the proof must include that join.

**Stable binding.** Define Bound as a cumulative accepted-history relation across the full replay horizon, not a mutable current-map lookup.  \(\Box(\operatorname{Bound}(k,h_1)\land\operatorname{Bound}(k,h_2)\Rightarrow h_1=h_2)\) for a key's full replay horizon. Hash equality is used within the stated cryptographic assumptions. A conflict does not become a new task automatically.

**Bounded obligation.** Equation (F19) is an admission and controlled-capacity-change condition, conditional on retained enforceable capacity. An uncontrolled capacity loss enters a visible degraded-capacity state, stops new admissions and preserves unresolved obligations pending authorized reconciliation; the inequality is not claimed to remain true through arbitrary physical loss. Actual consumption bounds and forecast feasibility are separate properties.

**No conclusion from silence.** If the observer's possible-value set for prior execution contains both zero and one, its externally reported status and retry action preserve that uncertainty. The system does not report nonexecution solely because a deadline passed.

**Verified reconstruction.** Accepted artifact bytes reconstruct the specified ordered object and satisfy its authenticated root, object binding, representation profile and semantic-validation requirements. This invariant establishes byte integrity within its assumptions, not scientific adequacy.

**No provenance multiplication.** A transfer or reuse record points to the original producing activity; it does not create an additional execution or independent-support assertion without corresponding evidence.

**Scoped continuation.** A continuation may consume only inputs whose present use is permitted and applicable. A result received before revocation is not a blanket permission for every later downstream task.

The following small traces distinguish genuine enforcement from plausible logs:

1. **Shared key, changed request.** Two authenticated frames use the same deduplication key but different workload or recipient fields. The second is rejected as a conflict, with no new provider effect.
2. **Lost reply after effect.** A provider performs an operation, its reply is lost, and the requester reconnects. Recovery reconciles the original identity; it does not treat the empty local result slot as permission to execute again.
3. **Reservation after lease expiry.** A worker loses its coordinator lease while a provider job continues. The new coordinator cannot reuse the physical reservation until a qualified stop/release or the resource owner's authoritative state supports it.
4. **Revocation race.** Revocation and one-use release arrive concurrently at the actual release owner. The resulting record exhibits one valid serialized order. A release ordered after revocation is refused; a prior release is retained as prior disclosure.
5. **Correct bytes, wrong use.** A result passes its digest and provenance checks but belongs to a different scope or forbidden purpose. Downstream use is denied without claiming the bytes are corrupt.
6. **Valid chunk, altered interpretation.** Bind the root, index, tree size and chunk ordering through the authenticated admitted manifest, and reject mismatches against that binding. A root-plus-inclusion-path alone need not distinguish all tree sizes: for leaf 0, siblings [L1,L2] can recompute the same root under sizes 3 and 4, since the verifier cannot tell whether L2 is a leaf digest or a subtree digest. The manifest-bound size, not a claimed universal property of inclusion proofs, supplies this rejection boundary.
7. **Many copies, one origin.** Several peers return the same originally produced answer. The receiver can use the redundancy for retrieval, but its evidence record retains one producing activity unless separate execution evidence exists.
8. **Offline correction.** A consumer holds a valid older artifact while a correction exists elsewhere. It records its known revision and freshness limitation instead of claiming globally current consensus.

These traces can guide future bounded qualification. They have not been executed in preparing this text. Passing them would support the corresponding boundaries under the tested profile; it would not prove resilience to every Byzantine participant, every timing schedule or every possible output leakage.


## Candidate operational specification

The following record and transition vocabulary is a proposed realization of the formal model, not an assertion of adopted wire schemas. K denotes a stable owner-scoped operation key, Q its exact immutable request digest, and J the effect-owner attempt. The concrete source profile in Appendix A must be kept distinct. [P2; P3; R-RPC]

## 17 Typed records and their authority

The following records are a minimal candidate logical model, not necessarily separate network messages. Field-level bounds and encodings remain profile obligations; Appendix A describes the actual bounded source schema. [P3; R-COSE]

- **Request R:** schema/version; operation namespace and identifier; intended receiver; purpose and job type; ordered input identities and representations; required transformation/model/tool identities; evidence and control-version requirements; requested bounds; original validity interval; permitted result recipients and onward-use restrictions; dependency identities; confidentiality mode. Input bytes may be carried inline or referenced, but referenced bytes must be resolved and verified before dispatch.
- **Admission A:** K and Q; receiving authority; current policy/grant references and revisions; actual selected configuration and resource-owner bindings; original deadline; local durable admission identifier; decision and refusal class. A is an attributable local decision, not a global authorization token.
- **Dispatch J:** A identity; exact executable request identity; authoritative effect owner; attempt identity; enforced limits; ownership generation if supported. J records the handoff to the boundary capable of producing the effect.
- **Result O:** producing J and Q; declared completion class; output representation, length and identity; actual available transformation/configuration evidence; output bytes or a retrievable authorized reference; limitations and partial-result indicators. A worker's claimed execution environment remains a claim unless supported by independently verified evidence.
- **Receipt T:** received O identity; observer; observed payload identity and length; verification outcome; local receipt event and available timing evidence. Receipt does not assert semantic correctness or independent replication.
- **Use U:** consuming task; O and T identities; applicability and present-use policy decision; analysis role; derived output identity; support, objections and unresolved uncertainty. U is a new use of prior work, not a second production of O.

Each record declares which fields are assertions and which were locally observed. Private prompts, identities and authority references are not automatically placed in a public manifest. Redacted public evidence is a separately identified derivative; it cannot be claimed byte-identical to the private original.

For a portable signed record, select a standard signature envelope and a complete cryptographic profile rather than signing an informal string concatenation. COSE defines signature structures and protected headers; a candidate profile would bind record type, version, intended audience and content identity in the authenticated payload or protected structure. Algorithm allowlists, key enrollment, key purpose and trust anchors remain local policy. [RFC 9052](https://www.rfc-editor.org/rfc/rfc9052.html). A valid signature proves attribution to an accepted key under its security assumptions, not entitlement, truthful execution, an independent witness or current permission. Channel-only authentication can support local observations but does not automatically produce a portable third-party-verifiable signature.


## 18 State transitions and effect boundaries

The candidate below operationalizes local linearization and RPC uncertainty, not an already established distributed transaction. [R-LINEAR; R-RPC]

A candidate receiver state is (K, Q, phase, owner generation, dispatch identity, retained outcome, local event sequence). This is a projection for exposition, not one scalar status that overwrites all other facts. A precise machine uses a product state: execution phase × dispatch knowledge × cancellation state × result availability × disclosure state. For example, execution may be complete while result bytes are currently unavailable, and cancellation may be requested while execution remains uncertain. The inspected source already distinguishes state, dispatch, cancellation and result availability; a candidate must preserve that distinction. The phase transitions are:

1. **UNSEEN → ADMITTED:** validate framing, authentication, request and current authority; atomically claim K for Q and durably retain A. Invalid traffic may create a bounded denial observation without creating an admitted operation.
2. **ADMITTED → DISPATCH_INTENT:** revalidate effect-time policy and original bounds; atomically record the exact J and consume the owner's local dispatch permission. A queue entry alone does not imply a provider invocation.
3. **DISPATCH_INTENT → RUNNING or EFFECT_UNCERTAIN:** submit J to the actual effect boundary. A positive owner observation can establish running. A connection failure cannot establish that submission had no effect.
4. **RUNNING/EFFECT_UNCERTAIN → OUTCOME_RETAINED:** reconcile authoritative owner state and capture the exact available outcome. Capture and its event binding commit together locally; an unverified reply is not sufficient.
5. **OUTCOME_RETAINED → DISCLOSED:** evaluate current result-disclosure rights and release the exact authorized representation. Delivery acknowledgment is a separate observation; its loss cannot erase a disclosure attempt.
6. **Received contribution → ACCEPTED_USE or REJECTED_USE:** the consuming node makes its own current applicability and policy decision, preserving the producing identity in either case.

Cancellation is a request to prevent future progression where enforceable. Before dispatch it may yield CANCELLED_NO_DISPATCH when the owner proves that state. After dispatch, CANCEL_REQUESTED is not CANCELLED_CONFIRMED; completed effects and already disclosed bytes remain historical facts. “Expired” records loss of authority for a transition, not proof of physical nonexecution. FAILED is used only with a stated observed failure and effect status; a timeout alone yields uncertainty.

These phases do not promise a universal order across machines. Local sequence numbers order durable events in one ledger. Causal references order dependencies; wall-clock timestamps, even when recorded, do not establish a total distributed order. Any freshness decision must state its clock source, accepted error, restart/epoch behavior and original cutoff. Reconnecting cannot renew the deadline.


## 19 Crash recovery replay and retention

The following deductions concern a local journal plus an external effect owner; compare classical RPC failure semantics and sink-side fencing. [R-RPC; R-LINEAR]

After restart, load the durable record for K before considering any network resubmission. If A exists without J, revalidation may permit dispatch under the unchanged original request and cutoff. If J exists but effect status is unknown, reconcile that same J with the authoritative effect owner. Do not issue a new attempt merely because an acknowledgment was lost. Where the effect owner cannot deduplicate or report the original attempt, safe nonduplication may require leaving the operation uncertain; availability is sacrificed rather than inventing an exactly-once guarantee.

The need for uncertainty can be shown by two indistinguishable recovery histories. In h₀, the worker crashes before invoking the provider; in h₁, the provider completes but its acknowledgment is lost before the worker records it. If both leave the same durable J and no externally queryable operation identity, the recovering worker cannot distinguish h₀ from h₁. Resubmission risks duplication in h₁; refusing resubmission risks noncompletion in h₀. Consequently, unconditional eventual completion and at-most-one external invocation cannot both be inferred from the local ledger alone. An idempotent/queryable effect boundary or stronger transaction protocol is an additional assumption, not an implication of hashing.

A transactional outbox closes the local gap between retaining an intent and scheduling its transmission, but it does not make an external provider invocation atomic with the local database. A fencing generation helps only if the actual effect boundary rejects stale generations. A lease held by the coordinator is not, by itself, a fence at the worker or provider.

Replay protection must outlive the period in which a replay could be accepted. Deleting the duplicate-suppression ledger while an old request is still admissible reopens the effect. A candidate therefore retains terminal tombstones through the accepted replay window, or uses a protected epoch transition that makes old requests permanently inadmissible. Restoring an old backup must not silently restore spent one-use authority. If rollback continuity cannot be established, the affected execution path remains held.

An authenticated duplicate request can receive an admission reconciliation response without being allowed to read current status or result bytes. Conversely, a newly authorized status observer does not obtain authority to execute the original request. Same-operation recovery is therefore an access-controlled operation, not an unlimited resend API.


## 20 Conflicting knowledge and protocol conflicts

This separation preserves the thesis’s epistemic and authorization distinctions. [P1 §§12–14; R-PROV]

Three cases require different treatment. An equal operation key with a different request digest is a protocol conflict and must not overwrite the original admission. A purported result whose bytes differ from its authenticated identity is an integrity failure. Two intact, authorized contributions that disagree are an epistemic conflict: retain both, their supporting evidence and dependence relations, and append a local evaluation rather than deleting the inconvenient result.

A correction is a new record that supersedes or contests a stated earlier claim within a stated scope. It cannot mutate the old object's bytes. A merge of immutable object identifiers can converge as a set while evaluations and permissions remain different at each node. There is no need to force a consensus truth bit. Neither last-writer-wins timestamps nor majority peer counts are justified truth rules, especially where peers share sources or one adversary controls many identities.

The provenance graph distinguishes entities (bytes and records), activities (production, transfer, verification, use) and accountable agents. This is consistent with the vocabulary of [W3C PROV-DM](https://www.w3.org/TR/prov-dm/); the candidate does not claim conformance to a particular PROV serialization. Every derived claim should expose its producing and supporting paths. Copying one result ten times creates ten custody observations, not ten independent experiments.


## 21 Invariants and discriminating tests

These are proposed safety and conditional-liveness obligations, not completed verification. [P1 §16; R-LAMPORT]

Under honest enforcement at the declared owner, durable local transactions, trusted enrollment and the selected cryptographic assumptions, the candidate aims to preserve:

- **Unique admission:** for any K, all admitted records refer to one Q.
- **No authority amplification:** a received record or valid signature alone cannot add local execution, disclosure or redistribution rights.
- **Exact binding:** retained result and use records refer to the actual verified request and representation identities, not merely a matching display label.
- **No renewal by retry:** reconnects, duplicate deliveries, key rotations and status queries cannot extend the original execution cutoff.
- **Monotone history:** new observations and corrections append; uncertainty is resolved only by evidence, not by changing the meaning of an earlier event.
- **Production/use separation:** reusing O creates U, never a counterfeit new production record for O.
- **Fail-closed confidentiality:** a confidential-required request has no transition to ordinary exposed execution.
- **Bounded admission:** malformed, repeated and incomplete traffic cannot create unbounded buffering, ledger growth or fan-out under the declared quotas.

A conditional liveness objective is also required: if the authenticated owners remain reachable, authority and resource availability persist through the original cutoff, required dependencies arrive, local scheduling is fair and the effect boundary eventually responds, an admitted eligible operation should reach a retained terminal outcome or a specified refusal. Removing these assumptions permits a safe indefinite hold or an unresolved outcome; the protocol must expose that distinction rather than report success.

These are proof obligations, not proved properties of the current implementation. For example, unique admission follows locally from an atomic uniqueness constraint over K together with digest comparison on every duplicate path; it does not follow across independent databases without a shared authoritative owner. Nonduplication of an external effect requires stronger downstream support than unique admission.

Qualification should inject crashes immediately before and after each durable write and external effect. Replay the same bytes across reconnects and key rotations; mutate one request field under the same K; present the same content under different encoding; send duplicate keys, oversized nesting and decompression bombs; reset the clock or restore an old ledger; revoke between check and consumption; race cancellation against dispatch; return correct bytes with wrong job identity; withhold an acknowledgment after successful execution; offer conflicting but correctly signed results; and attempt to use a retained status permission to disclose result text. Every case needs an expected state, allowed disclosure, event record and externally observed effect count. Include an adversarial worker that signs a false computation claim: the expected outcome is attributable but untrusted evidence, not automatic truth.


## 22 Discovery is a scoped control-plane problem

Let V(t) be the set of participating installations at time t and let G_s(t)=(V_s(t),E_s(t)) denote the authenticated communication graph permitted within scope s. Membership in a scope is not permission to execute a workload, receive its inputs, or join another scope. The relevant population for a lookup is therefore N_s=|V_s|, not necessarily the total number of installations. The existing commitment to overlapping scopes and sparse relevant-peer operation is compatible with several overlays, but does not determine one.

A full mesh has N_s(N_s−1)/2 undirected links, whereas a simple undirected graph with maximum degree d has at most N_s d/2. This algebra establishes a potential reduction in maintained adjacencies, not reachability or low lookup latency: a degree-bounded graph can be disconnected, and a connected path has diameter N_s−1. A scaling claim consequently needs a graph-construction rule, failure/repair model, bootstrap method, permission-constrained reachability definition, and routing algorithm.

Chord supplies a specific example in which identifier placement and maintained routing structure give logarithmic routing state and lookup communication with high probability under its assumptions. Kademlia supplies another, with XOR-distance routing and parallel asynchronous queries. Neither theorem transfers automatically to an arbitrary scoped or adversarial overlay. In particular, hashing node identifiers is not proof that an attacker cannot choose or multiply identities. [Stoica et al., 2001](https://snap.stanford.edu/class/cs224w-readings/stoica01chord.pdf); [Maymounkov and Mazières, 2002](https://pdos.csail.mit.edu/~petar/papers/maymounkov-kademlia-lncs.pdf).

For a proposed fixed-fan-out membership subsystem, let b be the complete expected bytes per local probe round, f the probe rounds per second, and u_s the scope's aggregate join/leave/update rate. Probe traffic alone is N_s b f bytes per second. If every update must reach every member, even a payload of h bytes entails at least (N_s−1)h receiving bytes per update, ignoring retransmission and framing, so aggregate update-delivery traffic is Ω(u_s N_s h). Fixed per-member probing does not imply bounded total churn dissemination. SWIM separates randomized failure detection from infection-style dissemination and achieves group-size-independent expected probe load and first-detection time under its model; that is not a constant-time guarantee that all nodes learn every change. [Das, Gupta and Motivala, 2002](https://www.cs.cornell.edu/projects/Quicksilver/public_pdfs/SWIM.pdf).

A candidate architecture is consequently hierarchical only in information scope, not necessarily in ownership: small local membership groups, bounded inter-scope discovery, expiring capability records, explicit peers that remain usable when optional directories fail, and task admission at the resource owner. This is a proposal consistent with the design, not a selected transport. A failed or partitioned directory should reduce discoverability rather than silently transfer execution authority to a relay.

## 23 Content distribution has physical lower bounds

The torrent analogy applies most directly to immutable objects and reusable artifacts. Chunk distribution can use concurrent suppliers and retain useful partial downloads, but should not be conflated with executing one model across machines. BitTorrent's original design provides an example of piece-oriented dissemination and peer-assisted upload; subsequent work shows that its incentive mechanism does not by itself prevent strategic exploitation. These are precedents for design questions, not a prescription to adopt BitTorrent or expose private artifacts publicly. [Cohen, 2003](https://pdos.csail.mit.edu/archive/6.824-2007/papers/cohen-btecon.pdf); [Piatek et al., 2007](https://www.usenix.org/conference/nsdi-07/do-incentives-build-robustness-bittorrent).

Consider the idealized distribution of an F-byte object initially present at one source to n recipients, all initially empty. Let u_0 be source upload capacity, d_i recipient download capacities, and u_i recipient upload capacities, all in useful payload bytes per second. If recipients may relay received bytes, there is no compression or preexisting side information, capacities are fixed, and protocol overhead is ignored, every completion time T satisfies

T ≥ max{F/u_0, F/min_i d_i, nF/(u_0+Σ_i u_i)}.

The first bound follows because each distinct object byte must leave the original source at least once; the second follows from each recipient's F-byte receive requirement; the third follows from the nF total receiving volume and total upload budget. This is an elementary cut/capacity lower bound, not a claim that a real swarm attains it. NAT relays, duplicate pieces, encryption framing, metadata, disk reads, hashing, heterogeneous policies and churn can raise the achievable time. With multiple initial complete sources, partial preexisting copies, coding or compression, the corresponding supply and cut constraints must be recomputed.

For an individual job j, let D_j denote uncached input and model bytes, b_j its measured effective transfer rate, and c_j its useful computation time. A minimal serial transfer-plus-compute model is T_j=D_j/b_j+c_j, before queuing and verification. Thus identical nominal FLOPS can yield radically different service rates when model placement changes. Warm-cache and cold-cache trials are different experimental conditions. Reuse benefits must include lookup, authorization, validation and retention costs and report the actual cache state, not assume all nodes already hold every artifact.

## 24 Task, pipeline and tensor parallelism are different hypotheses

Three forms of cooperation require separate claims. Task parallelism executes independent admitted jobs or independent branches of a task dependency graph. Pipeline/model parallelism assigns sequential model stages to devices and transfers activations between stages. Tensor parallelism divides operations within layers and typically introduces repeated collective communication. A three-role Analyst–Challenge–Synthesis workflow is not evidence of any particular model-parallel execution. If Challenge requires Analyst's output and Synthesis requires Challenge's result, these stages are causally sequential even when hosted by three machines.

For a fixed job graph with total compute work W measured in reference-processor seconds, p identical processors and critical-path work L, any schedule obeys T_p ≥ max(W/p,L). This work/span bound excludes communication and assumes processors implement the same workload. Adding nodes cannot shorten a fixed causal chain below L. In the simpler serial-fraction model, with fraction s of a fixed baseline time T_1 and nonnegative extra nonoverlapped overhead H(p), defined relative to this decomposition,

T_p ≥ T_1[s+(1−s)/p]+H(p),
S(p)=T_1/T_p ≤ 1/[s+(1−s)/p+H(p)/T_1].

This is an explicitly idealized Amdahl-style bound. It is inapplicable as a speedup comparison if the distributed run performs more reasoning, changes model quality, or uses a different acceptance criterion. [Amdahl, 1967](https://www.cs.cmu.edu/~18742/papers/Amdahl1967.pdf).

For a deterministic k-stage pipeline processing m independent microbatches, let τ_i be a stage's service time including any transfer that cannot overlap or run on an independent resource. With adequate buffers, independent stages, no failures, no resource contention and a regular schedule, ideal makespan is

T_pipe(m)=Σ_i τ_i+(m−1)max_i τ_i.

For balanced stages τ_i=τ, aggregate busy-time utilization is m/(m+k−1). When m=1, distributing stages does not remove their serial sum; for large m, throughput approaches 1/max_i τ_i. Additional communication resources, shared network links, backward passes or activation-memory limits require a different schedule model. GPipe is an empirical precedent for microbatch pipeline training, not proof of WAN speedup or of single-request latency reduction. [Huang et al., 2019](https://papers.neurips.cc/paper/8305-gpipe-efficient-training-of-giant-neural-networks-using-pipeline-parallelism.pdf).

For a layer boundary transporting a B-byte activation, a first-order one-way transport cost is ℓ+B/b, where ℓ is effective one-way latency and b effective payload bandwidth. It is not automatically a full RTT; request-response boundaries, acknowledgments and synchronization must be counted according to the actual protocol. Repeated autoregressive decoding can incur these boundary costs per token. Petals demonstrates that carefully partitioned large-model inference across heterogeneous Internet-connected devices can be useful under evaluated conditions, including abrupt disconnections. It does not establish arbitrary-node-count speedup or confidential execution on untrusted volunteer hardware. [Borzunov et al., 2023](https://arxiv.org/abs/2312.08361).

## 25 Capacity, queues, tails and admission control

Let λ_j be admitted external job arrivals per second for class j. Let a_ij denote the expected resource-i service seconds consumed per original class-j job, including retained and discarded attempts, retries and verification. For a resource providing c_i service-seconds per second, a necessary long-run rate-conservation condition is Σ_j λ_j a_ij ≤ c_i for every bottleneck resource i, assuming bounded long-run backlog and the stated finite service means. Strict slack, Σ_j λ_j a_ij < c_i, is a proposed operating requirement and a stability condition under suitable stochastic arrival/service and scheduling assumptions, not a universal necessity: deterministic arrivals exactly matching deterministic service can remain bounded at equality. Neither inequality alone is sufficient for every scheduling discipline or dependency graph. Increasing the number of nominal members is irrelevant when a required model, trusted owner, egress link, verifier or synthesis stage remains saturated.

For a stable stationary accounting system with finite means and a consistent arrival/departure boundary, Little's relation is L=λW: mean in-system population equals effective arrival rate times mean residence time. The same boundary must be used for all three quantities; admitted arrivals cannot be combined with queue occupancy that includes rejected arrivals. [Little, 1961](https://pubsonline.informs.org/doi/abs/10.1287/opre.9.3.383).

As an explicitly hypothetical M/M/1 example, Poisson arrivals at rate λ and independent exponential service at rate μ give mean total time 1/(μ−λ), provided λ<μ. Thus a server with 0.1-second mean service has 0.5-second mean total residence at 80% utilization and 2 seconds at 95%. This is a warning about saturation, not a fitted Triadic Brain latency prediction. Real model service times, batching, correlated bursts and retries generally violate the example's assumptions.

For independent identically distributed branch completion times with distribution F(t), an all-branches-required fan-out of k jobs completes by t with probability F(t)^k. If a single branch meets a deadline with probability 0.99, 100 independent required branches meet it with probability approximately 0.366. Dependence can change this drastically, and the equation does not apply to a first-success or quorum policy. Tail-latency amplification in large services motivates explicit deadline and fan-out accounting. [Dean and Barroso, 2013](https://research.google/pubs/the-tail-at-scale/).

Admission should therefore bound queued work, outstanding bytes, branch count, retries and local owner capacity rather than merely message size. Backpressure must propagate to the caller. A timeout is an observation of missing completion, not proof that the remote work did not execute; retries need idempotency or reconciled task identity and must be charged to the original workload's cost. Synchronous full-mesh coordination is not required by the design and should not be introduced accidentally through global status polling.

## 26 Availability, replication and churn

At a particular observation time, if complete replica i is retrievable with probability q_i and replica availability is independent, the probability of retrieving at least one complete copy is A=1−∏_i(1−q_i). For r equal-q replicas, achieving A≥A* requires r≥ceil[log(1−A*)/log(1−q)], with 0<q<1 and 0<A*<1. This is a point-in-time retrieval model, not a durability, confidentiality, correct-result or deadline guarantee.

Independence must be treated as an assumption to test. Shared power, account credentials, operator, provider, routing or software can correlate replicas. In an illustrative common-outage mixture, with probability c all replicas fail together and otherwise their independent availability is q, A=(1−c)[1−(1−q)^r], so replication alone cannot exceed 1−c. Placement across actual failure domains matters more than changing node labels.

If an object requires all C chunks, let A_c be the retrieval event for chunk c. Without any independence assumptions, the union bound gives P(all chunks available) ≥ max{0,1−Σ_c P(not A_c)}. Multiplying chunk availabilities is justified only with a defensible joint model. Overlapping placement usually couples them. For an erasure code requiring any k of n independently available shards with probability q, the toy availability is Σ_{i=k}^n binom(n,i)q^i(1−q)^(n−i); encoding overhead, reconstruction bandwidth and correlated domains remain separate costs.

For a single independently failing node with exponential failure rate δ, the probability of uninterrupted survival over duration t is exp(−δt). A k-stage pipeline requiring all assigned nodes to survive the entire same interval has probability exp(−tΣ_iδ_i), under that restrictive model. Stage-specific exposure intervals, replacement, checkpointing and correlated outages require a richer model. A long pipeline can therefore be less reliable than one node despite having greater total installed compute.

Repair is a capacity-consuming activity. If repair jobs arrive at average rate ν and move expected R bytes each across a bottleneck, average repair load is νE[R] bytes per second; this must fit alongside foreground demand with headroom. A positive margin is the proposed robustness requirement, not a universal mathematical necessity and not sufficient by itself, because correlated losses can generate bursts. Durable availability claims require measured detection delay, repair delay, replica/shard loss distributions and recovery behavior, not just a configured replica count.

## 27 Adversarial verification is not a count of agreeing nodes

Let p be a hypothetical probability that a sampled worker is Byzantine, with independent sampling from genuinely distinct administrative failure domains. For odd r redundant workers with an exact-output majority rule, the probability that a Byzantine majority is selected is Σ_{j=(r+1)/2}^r binom(r,j)p^j(1−p)^(r−j). This event is not identical to the probability of accepting a false semantic answer. Honest stochastic models may disagree, shared training or tools can correlate errors, and attackers can coordinate. Sybil identities invalidate the independent-sampling assumption; identity multiplicity cannot be equated with independent expertise or stake. [Douceur, 2002](https://www.microsoft.com/en-us/research/wp-content/uploads/2002/01/IPTPS2002.pdf).

For each bad result, let the audit-selection probability be a and the conditional detection probability given selection be d. If the combined detection events across n bad results are independent with these same probabilities, all escape with probability (1−ad)^n. Independent selection alone does not establish independent detection: a shared verifier blind spot or common adversarial strategy can correlate every miss. Without that additional independence assumption, the product formula is not justified. This is a proposed statistical model, not a security guarantee against adaptive adversaries who can recognize audits or concentrate on unauditable tasks. If exact verification is expensive, the compute, latency and privacy costs of recomputation must be included. Correct execution of a model also does not establish truth of its answer.

Classical Byzantine state-machine replication and cognitive review answer different questions. PBFT's replicated deterministic service uses 3f+1 replicas to tolerate f Byzantine replicas under its protocol assumptions; three role-labeled machines do not thereby tolerate one Byzantine replica. Agreement on an authorized state transition is not agreement that a natural-language conclusion is true. Its protocol and network assumptions must not be silently imported into Triadic Brain. [Castro and Liskov, 1999](https://www.usenix.org/legacy/publications/library/proceedings/osdi99/full_papers/castro/castro_html/castro.html).

Verification methods also have bounded applicability. Slalom demonstrates integrity/privacy techniques for selected neural-network computations with a trusted component and an untrusted accelerator. It does not establish a general zero-cost proof for arbitrary stochastic language-model reasoning or eliminate trusted-hardware assumptions. Any future verifiable-execution subsystem needs an exact function, numeric semantics, soundness bound, trust model, setup assumptions, overhead measurements and explicit treatment of input/output leakage. [Tramèr and Boneh, 2019](https://arxiv.org/abs/1806.03287).

## 28 Three machines to a million installations: a staged inference, not extrapolation

A million-installation population, a million simultaneously online workers, and a million-way single inference are three different propositions. Only a fraction may be reachable, authorized, compatible, warm, idle and appropriate for a particular job. Let I_i(t) indicate that node i satisfies all of these conditions. For a specified task class and resource with a common unit, aggregate eligible nominal capacity is Σ_i I_i(t)c_i(t), not N times an assumed representative capacity. This is an input to placement, not end-to-end usable capacity: shared links, sequential dependencies and owner restrictions remain separate constraints. Factoring the probability into online × authorized × compatible × idle probabilities is valid only if their dependence is modeled; these events are generally correlated.

A three-physical-node experiment can test concrete authenticated exchange, local owner admission, end-to-end result retention, cancellation/reconciliation, single-failure response and instrumented accounting. It cannot estimate million-node routing diameter, long-horizon churn, Sybil resistance, institutional failure correlation or ecosystem participation. Offline scripted node labels establish even less. Analytical bounds, simulation, emulation and physical deployment must remain separately labeled evidence classes.

A suitable evaluation ladder is: (1) source-bound protocol/model tests; (2) genuine distinct-host bilateral and triadic execution; (3) controlled multi-node emulation with specified latency, bandwidth, loss, churn and adversary distributions; (4) heterogeneous deployment with independently described failure domains; (5) calibrated large-population simulations with sensitivity analysis and held-out checks. Stage size is not a pass condition by itself. Advancement requires specified security, correctness, overload, recovery and accounting invariants plus measured performance under the declared workload. A million-node simulation, if eventually run, is evidence about that simulator and its assumptions, not a million-node deployment.

For comparable workloads, report at least: admitted/completed/accepted/discarded counts; quality under a preregistered rubric; end-to-end p50/p95/p99 latency; queue time; retries and duplicate work; payload and total wire bytes; discovery/control bytes; CPU/GPU seconds; measured energy where available; peak per-node memory separately from allocated cluster capacity; cold/warm cache status; detection/repair time; and deadline-qualified availability. Missing, withheld, unavailable and zero must remain distinct. A coordinator's monotonic clock can measure its workflow interval; subtracting unsynchronized host timestamps is not a valid duration estimate. Keep per-host clocks and cross-host uncertainty explicit.

Compare one-pass local, multi-role local and distributed multi-role conditions with matched task, model/generation settings, input lineage, rubric and quality target. Randomize run order and use paired trials where possible. Record failed and censored runs rather than silently dropping them. Report P(authorized accepted result by D | admitted job) over all admitted jobs and label latency quantiles conditional on successful acceptance separately. Unconditional eventual-success quantiles may be infinite or unidentifiable over a finite horizon. Informative timeout and cancellation cannot be treated as independent censoring without justification. Charge failed, duplicated, rejected-after-work and verification effort to the same workload boundary; zero accepted results makes cost per acceptance undefined or infinite, not zero. Strong scaling holds the workload fixed; weak scaling grows workload with resources. Total useful accepted work per joule, byte or device-second is not the same metric as elapsed-time speedup. Report confidence intervals and experimental units; repeated requests to one unchanged three-node installation are not independent samples of network deployments.

Claims about rare failures require appropriate sample sizes. Under independent Bernoulli trials with a fixed failure probability p and zero observed failures in n trials, a one-sided confidence bound at confidence 1−α is p≤1−α^(1/n). For α=0.05 and n=100 this is about 0.0295, not zero; the familiar approximation is 3/n. Correlated trials require an alternative model or block-level experimental units. No performance or correctness observation should be converted into an unlimited scale claim.


## 29 Trace refinement and reproducible protocol qualification

### 29.1 A conformance experiment is a composition claim

**P.** Let a test trace contain configuration identity, authenticated actors, exact input bytes, owner-policy versions, transport observations, durable events, external-effect observations and retained outputs. Define a projection from the concrete trace to the candidate abstract transition system. Conformance requires every projected transition to be permitted under the same request identity, original cutoff and current owner authority. A trace that replaces the disputed receiver or transport with a fixture provides evidence only about the substituted composition. This distinction is necessary when method, route, body and response contracts differ across modules, as in the frozen source audit. [P3; R-E2E; R-RPC]

The minimum interface-conformance matrix has rows for submission, status, cancellation, result retrieval, artifact retrieval, and supported configuration transitions; columns for caller, method/path, exact request body, authentication context, accepted response, error mapping, deadline owner and close/recovery owner. The matrix must be populated from actual producers and deciding consumers. Agreement on a type name is insufficient if one producer sends a reference while the consumer expects the full request, or one consumer returns a native admission record while the caller parses a status envelope. This matrix is a proposed verification artifact, not a new runtime registry. [P3](#p3)

### 29.2 Crash cuts and admissible recovery

The table describes candidate effect-boundary reasoning. It does not override the current sender's stricter refusal to resubmit an existing intent. A real implementation may remain held even where a stronger effect-owner protocol could establish safe progress. Every observation is scoped to the operation and owner that produced it. [P3; R-RPC]

| Crash or interruption cut | What is established | What is not established | Discriminating recovery obligation |
|---|---|---|---|
| Before durable local intent and before any external effect | No committed local intention under this trace | Nothing about an unrelated prior attempt | Recover local identity and verify that no earlier operation is being replaced |
| Intent durable but transmission not authoritatively observed | Exact local content and original operation exist | Whether bytes crossed an unobserved external boundary | Preserve original identity; do not infer nontransmission from missing receipt |
| Request transmitted but admission reply absent | A local transmission attempt | Remote receipt, rejection, durable admission or dispatch | Query the same operation through authorized owner reconciliation |
| Native admission committed but provider dispatch absent in an authoritative record | A retained accepted operation under that owner | That every other effecting path obeys the same journal | Revalidate current authority; prove the sole dispatch owner before any progression |
| Provider invocation may have occurred but no durable outcome exists | Dispatch uncertainty | Nonexecution, failure, quota refund or safe repeat | Hold or reconcile the original provider/effect identity |
| Result committed but acknowledgement lost | Owner's retained result, if its record is trusted | That the requester received or may disclose it | Retrieve under current status/result authority without creating another job |
| Key release or plaintext disclosure reply lost | An attempted disclosure boundary | Absence of disclosure or ability to recall it | Reconcile the same recipient/resource/attempt and preserve uncertainty |
| Chunk partially staged at deadline | Verified subset and bounded staging evidence | Complete object, safe decoding or fulfilled retention | Resume only within allowed policy; otherwise quarantine/expire under declared rules |
| Shutdown requested while worker or writer remains unresolved | A local stop request | Process termination, reservation release or exclusive-writer closure | Retain ownership and prevent conflicting successor until owner evidence resolves closure |

The trace should distinguish an error returned before a new side effect from the history of a previous attempt with the same operation identity. A present denial does not establish that an earlier authorized attempt never ran. Cancellation, expiry and revocation therefore need expected histories as well as expected final labels. [P3; R-RPC]

### 29.3 A discriminating test population

**P.** Freeze a finite test population and its expected outcomes before execution. For each case retain source/fixture identities, parser/profile versions, exact bytes, clock assumptions, injected versus real boundaries, allowed effects, observed effects, complete setup/call/teardown results, and cleanup observations. A collected test is not a passed test; a skipped adverse case is not negative evidence of a defect; an earlier passing snapshot is not current-tree parity. The qualification language of edition 1.2 supplies this evidence discipline. [P1 §2]

The population should include: duplicate keys and noncanonical representations; valid canonical values with wrong schema types; missing/extra fields; incompatible schema generations; altered request under the same operation identity; rotated pairing with an old operation; expired execution but separately permitted historical status; wrong result-disclosure hash; revocation racing effect consumption; two competing resource claims; late cancellation; lost result acknowledgement; oversized output with preserved completion history; partial transfer with aggregate staging pressure; correctly hashed chunk at wrong index; malicious manifest arithmetic; malicious but authenticated result text; correction after a downstream use; and a stalled close that must not authorize an overlapping successor. Expected outcomes should state admission, dispatch count, retained history, disclosure, resource occupancy and epistemic status separately. [P3; §§9–21]

Use model-based and property-based generation only within finite resource and side-effect bounds. Generate schedules around the named linearization points, not merely different natural-language prompts. A shrinking process must preserve the triggering authority and timing conditions; a smaller syntactic example that removes the relevant race is not the same counterexample. Seeds and generated traces support reproduction of the test, not reconstruction of unobserved hardware or stochastic model state. No such campaign was run to write this document. [R-LINEAR; P1 §16]

### 29.4 Spiral review and innovation disposition

**P.** An adversarial review round examines one frozen artifact and source boundary across protocol, mathematics, security, provenance and cognitive-architecture domains. Each finding records the violated claim, smallest counterexample, applicable source or assumption, proposed correction and expected discriminator. Repairs generate a new artifact identity and trigger affected re-review. A review that finds no issue contributes bounded inspection evidence, not a proof of perfection. [P1 §16]

The following hypotheses refine existing design objectives into candidate mechanisms. They are proposed research questions, not priority claims, selected implementations or new inventions of artifact reuse, Challenge, revisable provenance or owner reconciliation. Each study must freeze its workload, comparator, observation horizon, resource budget, scientific acceptance rule and statistical decision rule before outcomes are inspected. A failed safety invariant can refute a candidate directly; an underpowered or inconclusive utility estimate establishes neither benefit nor its absence. [P1 §§10.1,14.2–14.3,16; P2]

**H1: validity-partitioned reuse.** Separate cacheable checks on exact immutable bytes from checks whose answer depends on current rights, appraisal versions, time or intended use. A recipient-scoped index may memoize the former only under the complete representation and verification-profile identity; it must still obtain the latter from their current deciding owners. The comparator rechecks everything for the same permitted repeated-task workload. Primary endpoints are total verification and lookup resource use, accepted coverage and decision equivalence under the declared profile, including cold starts, invalidation, corrections and fallback. One accepted stale-rights use, cross-recipient cache leak or changed acceptance caused by omitting a required check refutes the safety claim. A predeclared positive-saving claim fails if the matched estimate and its specified uncertainty bound exclude the claimed saving; an interval crossing the decision threshold remains inconclusive. The candidate contribution is the particular partition and invalidation rule, not reuse itself. [P1 §14.3; §§6.1,9,15,17]

**H2: uncertainty-targeted Challenge.** Allocate a fixed exploration budget to the unresolved premises or donor-to-target relations most capable of distinguishing the retained alternatives, while recording prior-answer exposure and source dependence. Compare this with fixed-role or ordinary-clarification allocation using the same inputs, budget, stopping condition and adjudication procedure. Endpoints include detection of prespecified faulty premises, separately adjudicated useful new relations, preservation of sound conclusions and material dissent, and human review burden. A task distribution containing both seeded faults and sound controls makes indiscriminate objection observable. Budget overrun, unauthorized disclosure or erasure of required dissent rejects the candidate; the comparative utility claim is not supported unless the preregistered endpoint and noninferiority conditions are met. This extends the existing discovery spiral; active information-seeking already has substantial precedent, and its value depends on the assumed hypothesis space. [P1 §10.1; R-ACTIVE; R-DEBATE]

**H3: support-aware reopening.** After a correction, identify the affected present-use decisions while preserving alternative adequate support sets, instead of blindly invalidating every descendant or doing nothing. Compare the candidate with full reevaluation under the same frozen appraisal method, support graph and rights snapshot. Distinguish a correction to scientific support from an authorization revocation: replacement support does not legalize a forbidden use of the revoked input. Endpoint measures are agreement with the full-reevaluation oracle, required work, permitted correction traffic and delay until a consumer's view reflects the relevant change. A skipped decision that the oracle must reopen refutes the candidate's claimed completeness on that graph class; reduced work without equivalent decisions does not establish improvement. Finite generated cases must include conjunctive support, alternative support, common-source dependence, unavailable evidence and offline consumers. The proposed increment is an evaluated selective-update mechanism, not the original idea of revisable knowledge. Assumption-based truth maintenance is a relevant predecessor, not a proof of correctness for this authority-aware distributed setting. [P1 §14.2; R-ATMS; §§6.3,15.3,20]

**H4: owner-qualified release of stranded capacity.** Add only observations that the actual effect/resource owner can substantiate, binding the original attempt, ownership generation, remaining effect status and released resource dimensions. Compare against the current conservative hold under the same interruption schedules. Measure safely recovered capacity-time and completion opportunities, not simply shorter waits. An observation that permits overlapping live obligations, repeats an uncertain effect or mistakes a coordinator timeout for physical closure refutes the safety claim. A correct but permanently unavailable receipt can preserve safety while failing the liveness benefit. This is a candidate strengthening of the reconciliation contract, not a license to manufacture positive owner evidence. [R-RPC; R-LINEAR; §§12.3–12.4,13.3–13.4,19,29.2]

Code-facing findings must be classified separately. A real source mismatch between adjacent interfaces warrants a narrowly scoped repair and real-consumer test. A mathematical counterexample to a performance model warrants correction of the model, not an arbitrary runtime change. A threat requiring an unselected public overlay is a future design obligation, not proof that a bounded private-LAN implementation is currently vulnerable. This separation protects both engineering priority and scientific honesty. [P3](#p3)

## 30 Synthetic byte witness and layered rejection oracles

The following constructed object is intentionally not a complete peer-model request. It isolates canonicalization from application schema validation. Its two keys are ASCII; its value é is the single code point U+00E9; the final byte is LF. All lengths and digests below were computed over explicitly constructed UTF-8 bytes using ordinary byte hashing, without importing or executing product code. Expected parser behavior is a source-derived deduction, not a newly executed project test. [P3, Canonical profile and parser; R-JSON; R-UNICODE]

Canonical display, with the final newline shown symbolically:

```text
{"a":"é","n":1}\n
```

Exact hexadecimal bytes:

```text
7b2261223a22c3a9222c226e223a317d0a
```

The object is 17 bytes, with SHA-256 `55c561241405bf38857b42844132091edc90316851d158d0bc9b8f3e4d2acb7a`. The display characters backslash and n in the first exhibit denote the final newline rather than two literal bytes. The hexadecimal exhibit is authoritative for this synthetic witness. Its generic-canonical validity does not make it a valid model-job message. [P3](#p3)

| Vector | Change from the witness | UTF-8 bytes | Expected layer distinction |
|---|---|---:|---|
| V1 | None | 17 | Generic canonical object; not the full peer request schema |
| V2 | Put n before a | 17 | Same abstract JSON members but noncanonical key order in the inspected profile |
| V3 | Replace U+00E9 by U+0065 U+0301 | 18 | Canonically equivalent human text but non-NFC wire input, rejected rather than normalized |
| V4 | Remove terminal LF | 16 | Distinct bytes and rejected project-canonical representation |
| V5 | Insert a duplicate member a with the same value immediately after the first a and before n | 26 | Duplicate member rejected; identical repeated value does not cure ambiguity |
| V6 | Replace integer 1 by Boolean true | 20 | Generic canonical Boolean is possible; an exact-integer application field would reject it |

The V2 digest is `cf45f7faaaff8de12e63683ff776fe49faad55294af319a4fd9758fd1a38c794`; V3 is `bb7ecce56558e5546e8087d158bd7abecada578fde6d215240f677bec43651eb`; V4 is `f1899de414a50b27e5e783e8625531c113031f2dc3b4157f3bfad6d0d820509d`; V5 is `dff8cf29c4e0d5c5b88523edc942a424371626a1b1ce082f2791d265aef67a5c`; V6 is `9f1002c705dc8fa0762aa2156392f184ede87c31ca80b9d94400900d87b92360`. These are byte-identity examples, not enrolled signatures, authorization tokens or empirical security results.

The witness illustrates why a microscopic audit keeps four questions separate: can the bytes be framed; can they be decoded under the exact canonical profile; do they satisfy the message schema; and does an authenticated current owner permit their proposed effect? A negative answer at any layer has a different provenance and cannot be repaired by assuming success at another. The same distinction applies to result text: a valid string and exact digest do not establish an adequate scientific claim. [P3; P1 §13]

## 31 Conclusion and remaining obligations

The existing architecture is decentralized at the level of operational authority and deliberately selective at the level of cooperation. Its scientific object is not merely a network of model servers, but a governed circulation of representations, computational acts, support relations and revisable judgments. The microscopic account exposes exactly where that circulation requires a byte contract, a local owner decision, a durable effect record, a current-use check or a separate empirical inference. [P1; P2]

The resulting specification is not complete by declaration. Every unselected overlay, undefined resource-owner API, unavailable clock guarantee, unresolved key-release serialization, missing native interface join and unperformed deployment experiment remains an explicit obligation. A larger document cannot close those obligations. What it can do is make them inspectable, preserve the design's distinctive commitments, and specify observations capable of changing the assessment. Practical exit, provider choice, local usefulness, scoped cooperation and honest disagreement remain primary objectives even when their implementation costs more than a centralized alternative. [P1 §14.3; P2; P3]

## Appendix A Source defined bounded Challenge profile

**S/C/U.** This appendix reconstructs one frozen private source candidate. It is deliberately implementation-specific, not a proposed replacement protocol. Exact code identities and locators remain in the controlled source annex. No code is copied here; schemas and behavior are described analytically. The appendix is a sanitized analytical description; private source records are not embedded. Its snapshot is not a statement about later merged code, deployment or test results. [P3](#p3)

## A.1 Canonical representation and primitive domains

Let C(x) denote the project canonical JSON byte representation and H(b) SHA-256 over exactly bytes b. The implementation profile is UTF-8 without BOM, already-NFC text and keys, no surrogate code points, lexicographically sorted object keys, compact separators, finite numbers, and exactly one final LF. It uses Python JSON serialization with non-ASCII characters preserved. Parsing rejects duplicate keys, invalid UTF-8, nonfinite constants, absent LF, noncanonical whitespace/escaping/key order, and any input whose re-encoding differs from the original. **It rejects non-NFC text; it does not silently normalize wire input.** All hashes below include the canonical trailing LF when their input is C(x). This explicitly is not an RFC 8785 claim. [P3, Canonical profile and parser].

Canonical JSON generically admits exact JSON-compatible Python values, including integers and finite floats; individual protocol fields narrow those types. The general canonical serializer has no explicit structural-depth limit in this inspected implementation. The 65,536-byte peer frame bound does not by itself prove CPU/memory bounds for every parser case or cross-language numeric equivalence. A future interoperable standard must define these independently instead of labeling the current serializer JCS.

Peer primitives:

| Primitive | Exact accepted domain |
| --- | --- |
| Identifier | String matching [A-Za-z0-9][A-Za-z0-9._-]{0,127}; at most 128 ASCII characters |
| Digest | Exactly 64 lowercase hexadecimal characters |
| Operation ID | Exactly 32 lowercase hexadecimal characters |
| Integer | Exact integer type, excluding Boolean values |
| Pairing/grant version | Integer 1 through 2^31−1 |
| Timestamp | Integer milliseconds 1 through 2^53−1 |
| Text | Nonempty string, bounded by its UTF-8 byte length |
| Frame | Exact bytes, nonempty, at most 65,536 bytes, strict canonical top-level object |

Exact object-key sets reject both missing and extra fields. There is no extension-field escape hatch. The scope requires different sender and receiver identifiers. [P3, Wire primitives].

## A.2 Schema generations and complete request shape

Two generations coexist:

| Request | Status | Result |
| --- | --- | --- |
| control-anchor.peer-model-request.v1 | control-anchor.peer-model-status.v2 | control-anchor.peer-model-result.v1 |
| control-anchor.peer-model-request.v2 | control-anchor.peer-model-status.v3 | control-anchor.peer-model-result.v2 |

This is exact version selection from the request, not version negotiation or automatic fallback. The v2 request is a structured Challenge input with explicit output/sharing contracts. [P3, Schema identifiers]; [P3, response selection].

Every request has these fifteen common fields; version-specific additions follow:

1. schema_id.
2. sender_id.
3. receiver_id.
4. pairing_sha256.
5. pairing_version.
6. operation_id.
7. grant_sha256.
8. grant_version.
9. purpose.
10. created_at_ms.
11. not_after_ms.
12. expected_bindings.
13. input.
14. input_sha256.
15. limits.

A structured v2 request adds exactly output_contract_id and sharing_terms. Purpose is fixed to CHALLENGE_DRAFT; it is not an arbitrary tool or computation selector. not_after_ms must be later than created_at_ms by at most 120,000 ms. Syntax validation checks the original interval but not present-time eligibility; that is a separate current-authority check.

expected_bindings is an exact three-field object containing configuration_sha256, control_sha256, and provider_profile_sha256, all digests. limits is exactly output_tokens and result_bytes, integer ceilings respectively 1–4,096 and 1–32,768.

Legacy input is exactly draft and evidence, each nonempty UTF-8 text with ceilings 8,192 and 24,576 bytes respectively. The entire serialized frame must still fit the independent 65,536-byte bound, including escaped characters and metadata. input_sha256 must equal H(C(input)). [P3, Full request parser].

Structured input is exactly origin_manifest_sha256 and view. The former is a digest; the latter is an object whose schema_id equals control-anchor.peer-challenge-view.v1 and whose canonical representation is at most 24,576 bytes. output_contract_id must equal control-anchor.peer-challenge-output.v1.

A useful boundary: the wire parser verifies the structured view's type, schema name, and byte bound, but not its complete semantic shape. Native decoding invokes render_challenge_input, which invokes the deeper view verifier. That verifier requires the source/context/control/analyst bindings, exact reconstructed byte spans, appropriate included artifacts, analyst non-authority, and complete rather than silently truncated evidence. A parser-only claim must not be substituted for the downstream verification claim. [P3, Structured wire check]; [P3, native rendering join]; [P3, deep view verification]; [P3, rendering and context bound].

### Structured sharing terms

sharing_terms is exactly:

- schema_id = control-anchor.peer-challenge-sharing.v1.
- origin_manifest_sha256, equal to the request input's origin manifest digest.
- recipient_id, equal to sender_id.
- uses, a nonempty sorted, duplicate-free list drawn from INSPECT, SYNTHESIS, EXPORT.
- allow_cached_use, an exact Boolean.
- not_after_ms, in the timestamp domain and later than request.created_at_ms.

Syntactically requested terms are not yet accepted terms. Current receiver capabilities must separately allow the selected output contract and all requested uses, permit caching if requested, and bound sharing expiry. Sharing expiry is distinct from the job expiry; the parser does not require equality between them. [P3, Requested sharing terms]; [P3, current capability check].

## A.3 Identity, content, acceptance, and hash taxonomy

The implementation distinguishes several objects that should not be collapsed into a single job hash:

| Name | Meaning and actual producer |
| --- | --- |
| Pairing digest P | H(C(complete accepted MODEL peer-connection configuration)); includes the selected scope and transport configuration. Produced by model_scope, not by the peer's claim of identity. |
| Grant digest G | H(C(protected selected peer_model permission)); produced by the native permission projection, not issued by the wire parser. |
| Input digest I | H(C(request.input)); protects exact input representation. |
| Request digest R | H(C(full validated request)); binds scope, operation, grant, deadlines, pins, limits, input, and v2 terms. |
| Native intent key K | H(C({owner_id, receiver_id, operation_id})); owner is authenticated receiver-side identity, receiver comes from that authenticated scope. |
| Native record ID | Prefix PM- followed by K. |
| Native request digest N | H(exact native-envelope bytes), including receiver-selected routing/authorization and the original peer request. |
| Receipt digest E | The stored digest of the PEER_MODEL_INTAKE event; this event is part of the native event chain, not simply H(request). |
| Sharing digest S | H(C(request.sharing_terms)), bound into structured acceptance. |
| Result digest O | H(C(exact result envelope)), carried by COMPLETE/AVAILABLE status and verified against raw received result bytes. |
| Sender observation digest | H(exact bounded transport response bytes), including malformed complete bodies retained for diagnosis. Not an authority receipt. |

The request reference object contains the four scope fields, operation_id, grant_sha256, grant_version, purpose, and request_sha256. Status and result binding must canonical-byte-equal this reference; unknown fields cannot be smuggled into it.

K deliberately excludes pairing rotation, request hash, grant, and payload. Reusing the same authenticated owner/receiver/operation with changed content must conflict instead of silently becoming a fresh operation. This is a receiver-local namespace, not a global UUID registry or a network-wide proof of uniqueness. [P3, Pairing projection]; [P3, grant projection]; [P3, request reference]; [P3, native identity]; [P3, admission event and conflict].

E is computed by the existing event owner over a canonical row containing record_id, kind, actor, time, details, and previous-event digest; details also carry the event-runtime digest. The wire parser validates only that E is syntactically a digest when required. It does not receive/reconstruct that event or verify a signed global log. A receiver's authenticated transport response is therefore not independent proof of truthful custody. [P3, Native event digest]; [P3, receipt projection].

## A.4 Exact status and result constraints

Status has exactly eleven keys: schema_id, binding, state, receipt_sha256, acceptance, dispatch, cancellation, result_availability, result_sha256, reason, automatic_retry. automatic_retry must be false.

The acceptance object has exactly record_id, native_request_sha256, effective_bindings. The record ID is an identifier, native request hash a digest, and the effective bindings must equal the request's pins. Structured acceptance adds exactly output_contract_id and sharing_terms_sha256, equal to the selected output contract and H(C(request.sharing_terms)). Merely parsing this projection does not establish that a native transaction actually committed. [P3, Acceptance].

Allowed dispatch values are NOT_STARTED, STARTED, UNKNOWN. Allowed cancellation values are NOT_REQUESTED, REQUESTED, CANCELLED_BEFORE_DISPATCH, TOO_LATE, UNKNOWN. reason is null or an uppercase fixed-format token matching [A-Z][A-Z0-9_]{0,79}. receipt_sha256 and result_sha256 are null or digests subject to the following relationships:

| State | Receipt required? | Acceptance | Dispatch | Result availability | Required reason |
| --- | --- | --- | --- | --- | --- |
| RECEIVED | Yes | Must be null | NOT_STARTED | PENDING | No |
| ACCEPTED | Yes | Required | NOT_STARTED | PENDING | No |
| QUEUED | Yes | Required | NOT_STARTED | PENDING | No |
| DISPATCHING | Yes | Required | STARTED | PENDING | No |
| COMPLETE | Yes | Required | STARTED | AVAILABLE or UNAVAILABLE | If UNAVAILABLE |
| REJECTED | No | Must be null | NOT_STARTED | UNAVAILABLE | Yes |
| CANCELLED | Yes | Optional at wire level | NOT_STARTED | UNAVAILABLE | No |
| EXPIRED | No | Optional at wire level | NOT_STARTED | UNAVAILABLE | Yes |
| UNKNOWN | No | Required if dispatch=STARTED; otherwise optional | Any allowed dispatch value | UNKNOWN | Yes |

For every state, CANCELLED is equivalent to cancellation=CANCELLED_BEFORE_DISPATCH. A non-null result digest is required exactly when result_availability=AVAILABLE; otherwise it is forbidden. A digest requires acceptance and dispatch other than NOT_STARTED. Thus COMPLETE/UNAVAILABLE is a legitimate completed-execution observation with no releasable retained output, not permission to resubmit. The parser constrains one observation at a time. It does not implement cross-observation monotonicity, sequence numbers, quorum agreement, or a total distributed state history. [P3, Status parser].

Result has exactly eight keys: schema_id, binding, acceptance, text, review_status, execution_authority, new_call_authority, automatic_reuse. Before accepting a result, the parser fully revalidates the caller-supplied status, then requires COMPLETE/AVAILABLE; exact request reference; acceptance identical to status.acceptance; H(raw result bytes)=status.result_sha256; nonempty text within the request result-byte ceiling; review_status=UNREVIEWED; and all three authority/reuse flags false. Result text remains a string even in the structured result generation. The envelope alone does not establish semantic correctness or validate every proposed observation within that string. [P3, Result parser].

## A.5 Sender lifecycle and no-resend semantics

The sender is opt-in and defaults off. It accepts an owner-supplied httpx HTTPS client, with no URL userinfo/query/fragment and redirects disabled, plus a validated local PeerScope. The client owner remains responsible for actual TLS trust, credentials, bounds, and close observations.

Submission performs this ordering:

1. Parse exact request bytes and match local scope.
2. Sample monotonic time before wall-clock milliseconds; reject future/expired work.
3. Narrow the operation deadline to the lesser of the owner's deadline and the original request's remaining lifetime. Sampling order ensures descheduling consumes budget rather than renewing it.
4. If a durable intent file already exists, parse it and require byte-identical request content. Conflicts reject; identical content also refuses submission and permits inspection only.
5. Require fresh intent and journal paths; exclusively save exact request bytes.
6. Record a submission-attempt receipt before transport.
7. Make one exchange, check observed TLS/pairing metadata, retain/validate the response, then append an observation receipt.

The local file fence is durable for the selected namespace. It is not a global no-replay service; native identity/content checks are separately required across other clients or filenames. Safe file reads reject nonordinary/symlink/reparse/hardlink or unstable file identity; create-only writes preserve existing intent. [P3, Sender session and journal]; [P3, submit]; [P3, file read checks].

The shared clock guard accepts only a finite remaining operation interval greater than zero and no more than 120 seconds, including explicit inspection bounds. The shared exchange checks HTTP success before interpreting a body, forbids redirects and compressed response encoding, streams at most 65,536 raw bytes, and preserves an initiating error separately from an uncertain stream-close outcome. A malicious COMPLETE-shaped body on an HTTP error is not accepted as completion. File creation fsyncs the temporary file before create-only publication; this inspection does not establish every filesystem/power-loss persistence assumption. [P3, Clock and transfer limits]; [P3, raw exchange]; [P3, exclusive file publication].

The response observation requires a peer_tls_observation map containing matching pairing digest, TLSv1.2 or TLSv1.3, a certificate digest, and endpoint equal to the client base URL, together with pairing digest/version response headers. This is an injected transport observation contract, not TLS verification performed by peer_model_sender itself. A structurally valid certificate digest alone does not authenticate a peer. [P3, Observation check].

The attempt handler retains exact status bytes even when parsing rejects them. Rejected result bodies are retained separately; successful exact result envelopes use a stable result path and must match if already present. A transport, parser, deadline, or local receipt failure sets an **observation** to UNKNOWN and attempts an UNKNOWN journal event. It records whether sending was attempted and whether local receipt acknowledgement is known. It does not overwrite a remote native COMPLETE state, discard the original intent, or automatically resend. Failure to retain an already-rejected body is recorded as a distinct unknown outcome rather than replacing the original parse diagnosis. [P3, Attempt handling].

Explicit inspect loads the original intent and may operate after execution expiry under a fresh network-inspection bound; it does not renew execution time. Cancel writes a create-only cancel-intent marker before one cancellation request. Result retrieval requires a fully verified COMPLETE/AVAILABLE status and only returns retained inert output. None schedules polling, opens new work, or automatically executes the result. [P3, Inspection, cancellation, result].

## A.6 Receiver identity, admission, and transaction boundaries

The receiver is bound to one actual custody store. It is disabled by default; enabled attachment refuses a second intake object. receive parses the wire request, calls the current authenticator, requires the exact AuthenticatedPeer type, and matches all scope fields. It then constructs a receiver-owned native envelope using the authenticated owner, fixed local actor/control profile, provider authorization resolved from the store's actual configuration, and the peer request. Peer content cannot choose a native credential, service URL, arbitrary actor, or control route. [P3, Receiver attachment and receive].

Admission requires the registered intake context identity, matching actor, and CONFIGURED_PROVIDER mode. Within CustodyStore.write:

- If the record ID exists, stored request digest must match the candidate request exactly. An equal duplicate returns only immutable admission acknowledgement, marked receipt_only; it neither requeues nor discloses current live status.
- For a new record, total record and queue envelopes are checked.
- The real current control profile and configured provider profile are resolved.
- Their hashes and current store configuration hash must equal the peer's expected bindings.
- The exact native request, profile and runtime identity are stored in QUEUED state with the intake event.
- If a native owner is bound, current execution checking occurs within that same transaction before commit. A structured request requires a current owner at admission. A legacy intake without one can be held, but cannot gain dispatch authority from its receipt.

This transaction uses a writer lock and BEGIN IMMEDIATE; it rechecks actual schema/configuration/provider head under that writer lock and commits or rolls back on any BaseException. These are local custody atomicity mechanisms, not a distributed commit protocol. [P3, Admission implementation]; [P3, writer transaction].

The store explicitly describes its SQLite FULL/WAL durability as process-crash durability, not arbitrary power-loss protection. Use that bounded claim rather than treating a commit acknowledgement as universal hardware durability. [P3, Store durability scope].

## A.7 Current execution authority and one-use resource custody

CurrentModelGrant is only a typed projection. The wire validator checks exact scope, current grant hash/version/purpose, exact configuration/control/provider pins, created_at_ms ≤ now_ms < not_after_ms ≤ grant.valid_until_ms, and request ceilings no larger than current grant ceilings. Structured requests additionally require current output/sharing capabilities. Constructing this data class is not authentication, grant issuance, reservation, or permission. [P3, Current grant contract]; [P3, current validator].

The native check is called independently at ADMISSION, RELEASE, and CLAIM. It reconstructs the durable operation, checks both original and native request hashes, asks the actual owner for a fresh ExecutionCheck, and validates the owner's evidence references. A first check anchors a clock epoch in custody; subsequent checks must match it. It independently resolves the actual current control profile, compares store configuration and provider bindings, requires the provider's full per-request time to fit before the original request expiry, and rechecks provider authorization and effective output limits. [P3, Deciding native check]; [P3, release and claim call sites].

CustodyModelOwner insists on the exact store object, active transaction, actual database path, current protected configuration, application principal, actor, record, and retained native/request hashes. It calls a fixed native reader rather than trusting a peer-provided eligibility Boolean. authenticate requires both the current native application principal and the separate peer token; neither substitutes for the other. [P3, Fixed owner and authentication].

The Windows reader derives current permission from protected installation configuration and the actual guard-owned MODEL phase. The permission is optional and independently versioned; an artifact-reuse grant is insufficient. A permission selection contains owner/principal/scope, grant version, purpose, control selection and hash, provider hash, expiry, output and result ceilings; v2 adds output/sharing capabilities. The guard authenticates the requesting custody process by retained PID, creation time, and SID; authenticates the configured model profile; observes the actual phase before and after; and returns an observation without reserving or dispatching. [P3, Permission shape]; [P3, guard reader].

**Derived constraint, not a separate configured feature:** on this native path, provider maximum output tokens ≤ requested ceiling ≤ grant ceiling ≤ provider maximum output tokens. The first inequality comes from the native execution check; the middle from current grant validation; the last from permission validation. Thus all three must be equal for that fixed provider profile. Do not imply that the native serializer automatically lowers generation to any smaller requester-selected token ceiling. The result-byte ceiling is a distinct bound and does not have this same equality derivation. [P3, Native effective-output check]; [P3, request/grant ceiling]; [P3, grant/provider ceiling].

The nonrenewing clock uses the maximum of anchored wall time plus monotonic elapsed time, current wall time, and the previous high-water value. A negative monotonic interval rejects. The epoch is derived from the actual generation. Backwards wall-clock movement cannot replenish a job's expiry within that guard lifetime. This is not a demonstrated globally synchronized network clock or cross-restart clock service. [P3, Clock]; [P3, epoch and reader checks]; [P3, native client correlation].

At CLAIM, the custody owner binds a single intent to an already-owned MODEL phase in the same transaction as the native model-slot increment, provider serialization, transition to DISPATCHING, and DISPATCH_RESERVED_BEFORE_PROVIDER event. If a saved binding exists, its corresponding historical event must exist and match; a changed phase fails for lack of successor-continuity proof; another intent cannot reuse the phase. Removing only the compact current binding cannot erase historical use, because an extant binding event with missing head rejects. The binding is not written at ADMISSION/RELEASE when no prior claim exists.

The implementation contains a fail-closed successor condition, not a general implemented phase-handoff algorithm: a different phase remains held until a separately supported continuity mechanism exists. Result retention, cancellation, elapsed time, or timeout is not resource-closure evidence. The Job checks are enforced resource ceilings, explicitly **not physical RAM/VRAM preallocation**. [P3, Phase binding]; [P3, quota/dispatch commit]; [P3, native phase observation].

## A.8 Historical management, cancellation, result disclosure, and recovery

Execution and historical management are distinct authorities. access accepts only STATUS, CANCEL, RESULT; reparses the full original request; reauthenticates current peer identity; checks exact scope and saved owner/request hash; requires a bound owner; and asks it to authorize the action in the custody write transaction. Fresh management time does not renew the old execution window. An absent operation returns UNKNOWN_OPERATION_NO_RESUBMISSION rather than authorizing re-creation. Each eligible access is audited within the configured event budget. [P3, Historical receiver access].

There is a separate protected peer_model_access permission with own version and expiry, allowed actions, and exact result_disclosures. A result-disclosure entry binds request hash, result hash, control profile, and control hash. The actual owner derives these from the real custody row and exact outgoing result, checks that the capture event, raw response hash, extracted hash, active control and state agree, and asks the guard for current disclosure permission. This is stronger than accepting a requested digest as authority. Historical access does not reserve a new phase or consult the expired execution grant as if it were a new call. [P3, Access permission]; [P3, guard decision]; [P3, same-transaction outgoing-result binding].

Current scope equality still applies to historical access. Although K does not change with pairing rotation, the inspected access path does not demonstrate an automatic migration of old jobs to a new pairing scope. Do not infer rotation-safe historical readability from rotation-resistant deduplication.

Cancellation changes QUEUED to CANCELLED and records cancelled-before-dispatch. For other noncancelled states it records only cancellation requested, with inference_stopped=false and resource_release=false. Dispatch beginning first and cancellation beginning first are serialized by native custody ownership; there is no promise that a late cancellation stops inference or returns quota. [P3, Cancellation and projection].

Native CAPTURED maps to wire COMPLETE; FAILED and REFUSED map to UNKNOWN. Dispatch history is derived from the committed dispatch-reservation event, not guessed from payload availability. If retained payloads expire after dispatch, completion history can still project COMPLETE/UNAVAILABLE; otherwise uncertainty remains UNKNOWN. Expiration after a known cancelled-before-dispatch event maps back to CANCELLED. Oversize/nonrepresentable result text yields COMPLETE/UNAVAILABLE with a bound-specific reason rather than truncation or redispatch. [P3, Retained result]; [P3, status projection].

Gateway recovery transforms stranded DISPATCHING rows to UNKNOWN and records that inference may already have occurred. It does not queue another attempt. This supports conservative at-most-once intent handling under uncertainty, not exactly-once model execution or eventual successful completion. [P3, Recovery].

**R/U: protected-publication hold.** Exact-result validation exists, but a general post-capture protected-release transition is not operationally established at this snapshot. The retained handoff explicitly holds publication of a newly completed answer: changing business configuration to add its exact hash and reopening the existing store is not an authorized transition. Protected result-disclosure configuration and current-configuration checks make this a distinct lifecycle obligation, separate from the transport join and successor-phase hold. This is a source/handoff limitation, not a newly executed failure. [P3, retained handoff and protected owner configuration]; [P3, protected disclosure configuration]; [P3, current-store configuration check]

## A.9 Actual transport restrictions and the unestablished join

peer_connection validates either an explicit loopback pairing or an exact HTTPS endpoint using literal 127.0.0.1 or RFC1918 IPv4. It rejects DNS names, public routing, wildcard addresses, malformed ports, and extra config fields. LAN configuration binds the client address, public CA certificate, and bounded exact server certificate/key references. Server TLS is TLS 1.2 or later, with key logging disabled, no password-discovery prompt, and exact supplied file hashes. The native owner must still retain protected file/ancestor ownership across OpenSSL's path-based load; hashes alone do not eliminate replacement races. [P3, Configuration]; [P3, TLS construction].

The edge requires exact client IP, exact sole Host header, HTTPS for LAN, rejection of truthy Origin, Sec-Fetch-Site and Forwarded header values and rejection of every x-forwarded-* header name, and one bounded bearer token whose hash matches accepted pairing state. It rereads protected pairing configuration before exchange and again before native forwarding; any change denies. It does not create credentials, pairings, grants, sockets, background ownership, or listener admission merely by constructing the adapter. [P3, Edge authentication and recheck].

The edge serializes exchanges, retains an unresolved native worker if the requesting socket vanishes, shields that worker against a cancelled await, and rejects concurrent work while one operation remains unresolved. Mutating operation/path pairs are attempted at most once per adapter instance; the attempted-set ceiling is 128. STATUS/RESULT are classified as nonmutating by this edge resend fence even though transported as POST: they do not dispatch or cancel model work, but historical reads still append bounded access-audit evidence. The adapter owner’s lifecycle deadline and pairing expiry constrain all operations through this adapter; that deadline is distinct from the request’s execution expiry and does not contradict historical management under separately current authority. The first failure remains for the native lifecycle evidence owner. TLS handshake and full native worker cleanup require that external lifecycle owner, not just an ASGI timeout. [P3, No-resend edge lifecycle]; [P3, server lifecycle limitation].

### Concrete integration limit at this snapshot

The inspected native chain is consistently:

- Edge: POST /peer-model/requests, /peer-model/status, /peer-model/cancel, /peer-model/result.
- Application gateway: same four POST operations.
- Custody: same four POST operations.
- All carry the **entire original canonical request**; query strings and alternate raw-path encodings reject.
- Submission returns a native custody admission representation; historical STATUS returns the strict wire status projection.

By contrast peer_model_sender submits to POST /peer-model/jobs, inspects with GET /peer-model/jobs/{operation_id}, cancels with POST /peer-model/jobs/{operation_id}/cancel carrying only a request reference, and fetches result with GET /peer-model/jobs/{operation_id}/result. Reads carry request/grant query parameters. Its submission handler expects a strict wire status response.

Therefore **these inspected sender and native routes are not directly interoperable as written**. No translating adapter was found in the inspected chain, and this read-only source analysis did not search every unrelated repository file or run an end-to-end exchange. This is an identified source-level join gap, not a new executed regression result. It must not be hidden by describing the combined modules as a complete operational peer service. [P3, Sender routes/expectations]; [P3, edge routes]; [P3, native routes/response]; [P3, gateway].

Read-only test inspection reinforces the evidence boundary: sender tests use a simulated receiver with /jobs conventions and httpx.MockTransport, while native route/service tests use the four POST operations and injected HTTP/native observations. Their existence does not demonstrate that the sender reaches the real native deciding consumer. [P3, Sender fixture]; [P3, service seam]; [P3, joined factory seam].

The existing concrete peer_tls_client in peer_artifact_transfer is also artifact-specific at this snapshot: it reads use_id, permits only peer-receiving artifact routes, and checks the artifact grant. It correctly constructs CA-verified TLS with retries=0 and real TLS observations, but that does not integrate the MODEL sender. A repaired sender must be assessed against the real permitted transport contract too. [P3, Concrete TLS route restrictions and construction].

## A.10 Error and uncertainty boundaries

There are layered, intentionally different failure vocabularies:

- CanonicalError is a ValueError subclass with fixed canonical/file error codes, e.g. duplicate member, non-NFC text, invalid UTF-8, noncanonical bytes, unsafe or changed files.
- The pure peer contract emits ValueError with PEER_MODEL_ reasons; these reject malformed frames, inconsistent bindings/states, changed capabilities, or inert-result violations.
- Native receiver fail emits ServiceError with PEER_MODEL_ and status 403. Admission/access/service exceptions can roll back the write transaction.
- Native Windows expected permission denial uses ModelPermissionDenied, distinguished from uncertain transport/ownership failure.
- The edge maps authentication, routes, body, deadline, duplicate/unresolved operation and native ambiguity to bounded HTTP error responses; automatic_retry=false is explicit.
- Gateway/native routes return 422 for rejected canonical requests, 404 for unexposed/extraneous routes, 403 for invalid authenticated context, and 503 for uncertain/bounded-response failures.
- Sender observation failure does not assert execution failure or overwrite remote outcome; it preserves uncertainty and blocks automatic resubmission.

An error code is not by itself proof of when an external side effect occurred. Classification depends on whether execution crossed the durable dispatch boundary and what was independently observed. Even a successfully committed native result can coexist with an UNKNOWN local delivery/receipt observation. [P3, Pure error boundary]; [P3, native fail]; [P3, permission denial type]; [P3, sender uncertainty].


## Primary references and project evidence

References support the adjacent, bounded claims. Citing a protocol, theorem or predecessor system does not assert adoption, conformance or inherited performance. Newly proposed requirements and elementary deductions are identified as such rather than attributed to unrelated literature.

<a id="p1"></a>**P1.** Prislac, T. *Triadic Brain from Byte Identity to Revisable Knowledge*, edition 1.2, 3 November 2026. [Frozen public manuscript](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/23a674cab2af23baae6e74af2aaf5c7c934ff473/docs/papers/triadic-brain-micro-spectrum/2026-11-03-edition-1.2/TRIADIC_BRAIN_MICRO_SPECTRUM.md). Preparation-time draft metadata is preserved in the publicly accessible source; this supplement does not overwrite it.

<a id="p2"></a>**P2.** Prislac, T. Existing master design §17.5 and §17.5.1, including owner clarification dated 9 October 2026; P2P development map and 24-requirement code crosswalk; concept reference §6; confidential task-key-release plan. Controlled project sources, exact versions and source positions retained in a separate private annex. These support architecture provenance and bounded source claims, not public independent reproduction. No private operational record is embedded here.

<a id="p3"></a>**P3.** Frozen peer-model source reconstruction, 4 November 2026. Exact canonicalization, wire, sender, receiver, edge and native-owner files were inspected at one retained candidate. The controlled source annex binds identities and line ranges. The account is source-only, not an executed integration test; later code changes are separate evidence.

<a id="r-e2e"></a>**R-E2E.** Saltzer, J. H., Reed, D. P. and Clark, D. D. *End-to-End Arguments in System Design*. ACM Transactions on Computer Systems, 1984. [Author-hosted paper](https://web.mit.edu/Saltzer/www/publications/endtoend/endtoend.pdf).

<a id="r-rpc"></a>**R-RPC.** Birrell, A. D. and Nelson, B. J. *Implementing Remote Procedure Calls*. ACM Transactions on Computer Systems, 1984. [Original paper](https://www.cs.cmu.edu/~dga/15-712/F07/papers/birrell842.pdf). Compare binding, call identity and failure semantics; the project's state machine is not the paper's implementation.

<a id="r-lamport"></a>**R-LAMPORT.** Lamport, L. *Time, Clocks, and the Ordering of Events in a Distributed System*. Communications of the ACM, 1978. [Author-hosted paper](https://lamport.azurewebsites.net/pubs/time-clocks.pdf).

<a id="r-linear"></a>**R-LINEAR.** Herlihy, M. P. and Wing, J. M. *Linearizability A Correctness Condition for Concurrent Objects*. ACM Transactions on Programming Languages and Systems, 1990. [Author-hosted paper](https://cs.brown.edu/~mph/HerlihyW90/p463-herlihy.pdf).

<a id="r-flp"></a>**R-FLP.** Fischer, M. J., Lynch, N. A. and Paterson, M. S. *Impossibility of Distributed Consensus with One Faulty Process*. Journal of the ACM, 1985. [Original paper](https://groups.csail.mit.edu/tds/papers/Lynch/jacm85.pdf). The asynchronous deterministic termination result has specific crash/message assumptions; it is not a blanket prohibition of decentralized agreement.

<a id="r-prov"></a>**R-PROV.** Moreau, L. and Missier, P., eds. *PROV-DM The PROV Data Model*. W3C Recommendation, 2013. [Recommendation](https://www.w3.org/TR/prov-dm/).

<a id="r-json"></a>**R-JSON.** Bray, T., ed. *The JavaScript Object Notation Data Interchange Format*. RFC 8259, 2017. [Standard](https://www.rfc-editor.org/rfc/rfc8259.html).

<a id="r-jcs"></a>**R-JCS.** Rundgren, A., Jordan, B. and Erdtman, S. *JSON Canonicalization Scheme*. RFC 8785, 2020. [Informational specification](https://www.rfc-editor.org/rfc/rfc8785.html). The project canonicalizer is not asserted to conform to JCS.

<a id="r-cbor"></a>**R-CBOR.** Bormann, C. and Hoffman, P. *Concise Binary Object Representation*. RFC 8949, 2020. [Standard](https://www.rfc-editor.org/rfc/rfc8949.html). An unadopted comparison; deterministic encoding requires a selected profile.

<a id="r-cose"></a>**R-COSE.** Schaad, J. *CBOR Object Signing and Encryption Structures and Process*. RFC 9052, 2022. [Standard](https://www.rfc-editor.org/rfc/rfc9052.html). A possible portable-envelope family, not a selected migration.

<a id="r-unicode"></a>**R-UNICODE.** Unicode Consortium. *Unicode Normalization Forms*, Unicode Standard Annex 15, revision 58, 2026. [Versioned specification](https://www.unicode.org/reports/tr15/tr15-58.html). A deployment must pin the normalization behavior it actually uses; citation of this revision does not identify the project's runtime Unicode database.

<a id="r-tcp"></a>**R-TCP.** Eddy, W., ed. *Transmission Control Protocol*. RFC 9293, 2022. [Standard](https://www.rfc-editor.org/rfc/rfc9293.html).

<a id="r-httpsem"></a>**R-HTTPSEM.** Fielding, R., Nottingham, M. and Reschke, J., eds. *HTTP Semantics*. RFC 9110, 2022. [Standard](https://www.rfc-editor.org/rfc/rfc9110.html).

<a id="r-http1"></a>**R-HTTP1.** Fielding, R., Nottingham, M. and Reschke, J., eds. *HTTP/1.1*. RFC 9112, 2022. [Standard](https://www.rfc-editor.org/rfc/rfc9112.html).

<a id="r-uri"></a>**R-URI.** Berners-Lee, T., Fielding, R. and Masinter, L. *Uniform Resource Identifier Generic Syntax*. RFC 3986, 2005. [Standard](https://www.rfc-editor.org/rfc/rfc3986.html).

<a id="r-tls"></a>**R-TLS.** Rescorla, E. *The Transport Layer Security Protocol Version 1.3*. RFC 8446, 2018. [Standard](https://www.rfc-editor.org/rfc/rfc8446.html), particularly §8 on replay and early data.

<a id="r-aead"></a>**R-AEAD.** McGrew, D. *An Interface and Algorithms for Authenticated Encryption*. RFC 5116, 2008. [Standard](https://www.rfc-editor.org/rfc/rfc5116.html).

<a id="r-hkdf"></a>**R-HKDF.** Krawczyk, H. and Eronen, P. *HMAC-based Extract-and-Expand Key Derivation Function*. RFC 5869, 2010. [Informational specification](https://www.rfc-editor.org/rfc/rfc5869.html).

<a id="r-rats"></a>**R-RATS.** Birkholz, H. et al. *Remote ATtestation procedureS Architecture*. RFC 9334, 2023. [Informational architecture](https://www.rfc-editor.org/rfc/rfc9334.html). Roles, appraisal and freshness are distinct from the proposed owner-side key-consumption protocol.

<a id="r-kms"></a>**R-KMS.** Amazon Web Services. *Cryptographic attestation support in AWS KMS*. [Official attested-call documentation](https://docs.aws.amazon.com/kms/latest/developerguide/attested-calls.html). Concrete recipient-key/attestation precedent, not an adopted service or a spending authorization.

<a id="r-kad"></a>**R-KAD.** Maymounkov, P. and Mazières, D. *Kademlia A Peer-to-Peer Information System Based on the XOR Metric*. IPTPS, 2002. [Original paper](https://pdos.csail.mit.edu/~petar/papers/maymounkov-kademlia-lncs.pdf).

<a id="r-sybil"></a>**R-SYBIL.** Douceur, J. R. *The Sybil Attack*. IPTPS, 2002. [Original paper](https://www.microsoft.com/en-us/research/wp-content/uploads/2002/01/IPTPS2002.pdf).

<a id="r-swim"></a>**R-SWIM.** Das, A., Gupta, I. and Motivala, A. *SWIM Scalable Weakly-consistent Infection-style Process Group Membership Protocol*. DSN, 2002. [Original paper](https://www.cs.cornell.edu/projects/Quicksilver/public_pdfs/SWIM.pdf).

<a id="r-libsec"></a>**R-LIBSEC.** libp2p maintainers. *Security considerations*. [Official documentation](https://libp2p.io/docs/security-considerations/). Implementation guidance, not evidence of this project's resistance to the listed attacks.

<a id="r-ice"></a>**R-ICE.** Keränen, A., Holmberg, C. and Rosenberg, J. *Interactive Connectivity Establishment A Protocol for Network Address Translator Traversal*. RFC 8445, 2018. [Standard](https://www.rfc-editor.org/rfc/rfc8445.html).

<a id="r-turn"></a>**R-TURN.** Reddy, T., Johnston, A., Matthews, P. and Rosenberg, J. *Traversal Using Relays around NAT Relay Extensions to Session Traversal Utilities for NAT*. RFC 8656, 2020. [Standard](https://www.rfc-editor.org/rfc/rfc8656.html).

<a id="r-dcutr"></a>**R-DCUTR.** libp2p maintainers. *Direct Connection Upgrade through Relay*. [Official documentation](https://libp2p.io/docs/dcutr/).

<a id="r-relay"></a>**R-RELAY.** libp2p maintainers. *Circuit Relay v2*. [Protocol specification](https://github.com/libp2p/specs/blob/master/relay/circuit-v2.md), with [connection/privacy explanation](https://libp2p.io/docs/circuit-relay/).

<a id="r-ipfspriv"></a>**R-IPFSPRIV.** IPFS maintainers. *Privacy and encryption*. [Official documentation](https://docs.ipfs.tech/concepts/privacy-and-encryption/).

<a id="r-ipfs"></a>**R-IPFS.** Benet, J. *IPFS Content Addressed, Versioned, P2P File System*. 2014. [Original design paper](https://arxiv.org/abs/1407.3561). Persistence behavior also requires the [official retention/pinning documentation](https://docs.ipfs.tech/concepts/persistence/).

<a id="r-bt"></a>**R-BT.** Cohen, B. *The BitTorrent Protocol Specification*, BEP 3. [Primary specification](https://www.bittorrent.org/beps/bep_0003.html). Its historical SHA-1 piece-digest choice is not a recommendation for a new protocol.

<a id="r-macaroons"></a>**R-MACAROONS.** Birgisson, A. et al. *Macaroons Cookies with Contextual Caveats for Decentralized Authorization in the Cloud*. IEEE Symposium on Security and Privacy, 2014. [Author publication page](https://research.google/pubs/macaroons-cookies-with-contextual-caveats-for-decentralized-authorization-in-the-cloud/); [full paper](https://theory.stanford.edu/~ataly/Papers/macaroons.pdf). Attenuated delegation comparison, not a selected credential format.

<a id="r-drf"></a>**R-DRF.** Ghodsi, A. et al. *Dominant Resource Fairness Fair Allocation of Multiple Resource Types*. NSDI, 2011. [Primary publication](https://www.usenix.org/conference/nsdi11/dominant-resource-fairness-fair-allocation-multiple-resource-types). Multi-resource allocation comparison, not a fairness proof for an adversarial WAN.

<a id="r-petalssec"></a>**R-PETALSSEC.** Petals maintainers. *Security, privacy, and AI safety*. [Official guidance](https://github.com/bigscience-workshop/petals/wiki/Security,-privacy,-and-AI-safety).

<a id="r-debate"></a>**R-DEBATE.** Du, Y. et al. *Improving Factuality and Reasoning in Language Models through Multiagent Debate*. ICML, 2024. [Primary publication](https://proceedings.mlr.press/v235/du24e.html). Task-specific experimental comparison, not a universal independence or correctness theorem.

Additional primary citations are provided inline in the formal storage and scaling sections. Every reference's role is bounded by the adjacent text; no third-party benchmark is substituted for a Triadic Brain observation.

<a id="r-injection"></a> **R-INJECTION.** Greshake, K., Abdelnabi, S., Mishra, S., Endres, C., Holz, T., and Fritz, M. (2023). *Not what you’ve signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection*. arXiv:2302.12173v2. https://arxiv.org/abs/2302.12173v2. Primary attack research; cited for threat evidence, not as proof of the proposed containment architecture.

<a id="r-tuf"></a> **R-TUF.** The Update Framework specification, version 1.0.37, 8 October 2026, §§1.4–2.2 and 5. https://theupdateframework.github.io/specification/latest/. Primary update protocol and threat model; comparative reference, not an adopted project dependency.

<a id="r-active"></a> **R-ACTIVE.** MacKay, D. J. C. (1992). *Information-Based Objective Functions for Active Data Selection*. Neural Computation 4(4), 590–604. DOI 10.1162/neco.1992.4.4.590. [Institutional full-paper record](https://authors.library.caltech.edu/records/efefp-2j353). Prior work on measurement selection under a Bayesian hypothesis model; not a claim that Triadic Brain implements that model or inherits its utility.

<a id="r-atms"></a> **R-ATMS.** de Kleer, J. (1986). *An Assumption-based TMS*. Artificial Intelligence 28(2), 127–162. DOI 10.1016/0004-3702(86)90080-9. [Author-hosted original paper](https://www.dekleer.org/Publications/An%20Assumption-Based%20TMS.pdf). Prior work on assumption sets and multiple support contexts; not a distributed rights-enforcement protocol or a scientific-truth oracle.
