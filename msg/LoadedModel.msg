# Latched snapshot of the model cached on a MANAGED policy server, published
# by the server's owning node (rosetta_client_node, ~/loaded_model,
# transient-local QoS so late subscribers receive the last value).
#
# Scope: the publisher is the server's single owner (it spawned the
# subprocess and is its only gRPC client), so this mirror is authoritative
# for that server. Servers at an independent server_address have other
# clients and are NOT observable from here — goals sent to them never
# update this message. The mirror updates when the owner acts (load,
# preload, start/stop/restart, noticing an exited subprocess); between a
# silent server crash and the owner's next action the value can be stale.

uint8 STATE_UNKNOWN=0   # No managed server (launch_local_server false); a
                        # remote server's cache cannot be observed honestly.
uint8 STATE_NONE=1      # Managed server running with an empty cache, or
                        # stopped/exited (nothing is warm either way).
uint8 STATE_CACHED=2    # The model below is warm in the managed server's
                        # checkpoint cache; a goal for it skips the cold load.

builtin_interfaces/Time stamp     # Node clock at publish time
string server_address             # The managed server this snapshot describes
uint8 state
string policy_type                # Resolved architecture (sns_smolvla, act, ...);
                                  # part of the cache identity — the same path
                                  # loaded as a different type is a different model
string policy_name                # Registry entry name; empty when the goal
                                  # supplied an explicit path instead
string pretrained_name_or_path    # Empty unless state is STATE_CACHED
