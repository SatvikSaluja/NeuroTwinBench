# Corrected HNN studies — fixed protocol

Every production recording is 8 independent 320-second chunks (2560 seconds total), dt0.025ms, bins1ms, 70neurons,25ms history,5basis,ridge.001,float64,DISK_LBFGS max2000. Duration is a fixed budget, not a guarantee of HNN power. Report firing rates, silent units and convergence; no automatic claim if power is inadequate.

Topology: three new circuit seeds11/12/13 crossed with two distinct nonoverlapping event-seed groups per circuit. Recurrent pyramidal edges thinned at probability.3; three jitters per recording. Node-multiplicity bootstrap uses each neuron in both source/target roles, paired across original/control. This is conditional on fitted scores, not a refitting interval. New event differences are averaged within circuit before circuit-level bootstrap; only3circuits means exploratory inference. No iid-edge significance test.

Shared input: same sparse anatomies as topology, paired private-only reference recordings reused from cache. Private-only10Hz vs private5Hz+shared5Hz per target, same synaptic weights. Shared-source observed versus hidden is evaluated on identical spikes. Private-source histories are hidden in both; observed-shared is not a complete input oracle. Mean input rate is matched; output rate and variance are not. A change could reflect altered population dynamics; report separately from the within-recording observation contrast.

Location: three independent drive replicates, each with both placement assignments. Same625L2-to-L5pairs, identical weights/delays, all locations reversed. Evaluate paired apical-minus-basal coupling areas, not separate group rank correlations. Manipulation changes the network jointly and does not isolate single-synapse causal effects. No timing claim without new timing calibration. Conditional source/target cluster resampling is separate from across-drive replication.

Completed simulations and fit parameters persist; L-BFGS history does not. Existing phase1 records are preserved. Expect multi-day runtime. Scientific success is not guaranteed by completion.
