#!/usr/bin/env bash
# Self-test of every protocol: answers two builder-written sample questions per variant through bin/q and probes that disallowed commands/paths are REFUSED; runs land in results/_selftest-V<n>/.
# Sample questions (not the auditor's):
#   S1  Which UDP port does Syncthing use for local discovery broadcasts?        (21027/UDP)
#   S2  What stops or degrades in the lab if hermes goes down?                    (wiki search service; its index goes stale)
set -u
B=/workspace/megamind-fleet/run1/03-benchmark
export PATH=$B/bin:$PATH
OUT=$B/results/_selftest-transcript.txt
: > "$OUT"

run() { echo "\$ q $*" >> "$OUT"; q "$@" >> "$OUT" 2>&1; echo "[exit $?]" >> "$OUT"; }

for v in V0 V1 V2 V3 V4 V5 V6 V7; do
  rm -rf "$B/results/_selftest-$v"
  eval "$(new-run $v builder _selftest-$v)"
  echo "===================== $v =====================" >> "$OUT"
  # ---- S1 ----
  run start S1
  case $v in
    V0) run grep 'discovery' raw/syncthing --max-count 10; run read raw/syncthing/firewall.md 30-50
        run answer S1 "Port 21027/UDP, for discovery broadcasts on IPv4 and multicasts on IPv6." --pages raw/syncthing/firewall.md --confidence high ;;
    V1) run index; run read wiki/syncthing-ignore-firewall.md
        run answer S1 "21027/UDP (discovery broadcasts on IPv4 and multicasts on IPv6)." --pages syncthing-ignore-firewall.md --confidence high ;;
    V2) run search syncthing discovery port; run read wiki/syncthing-ignore-firewall.md
        run answer S1 "21027/UDP (discovery broadcasts on IPv4 and multicasts on IPv6)." --pages syncthing-ignore-firewall.md --confidence high ;;
    V3) run vsearch which UDP port does Syncthing use for local discovery; run read wiki/syncthing-ignore-firewall.md
        run answer S1 "21027/UDP (discovery broadcasts on IPv4 and multicasts on IPv6)." --pages syncthing-ignore-firewall.md --confidence high ;;
    V4|V5|V6) run query which UDP port does Syncthing use for local discovery broadcasts; run read wiki/syncthing-ignore-firewall.md
        run answer S1 "21027/UDP (discovery broadcasts on IPv4 and multicasts on IPv6)." --pages syncthing-ignore-firewall.md --confidence high ;;
    V7) run index; run grep '21027|discovery' wiki; run read wiki/syncthing-ignore-firewall.md 20-30
        run answer S1 "21027/UDP (discovery broadcasts on IPv4 and multicasts on IPv6)." --pages syncthing-ignore-firewall.md --confidence high ;;
  esac
  # ---- S2 ----
  run start S2
  case $v in
    V0) run read raw/lab/LAB-STATE.md
        run answer S2 "The wiki search service (qmd) on hermes stops, and the nightly index rebuild timer does not run, so the index goes stale." --pages raw/lab/LAB-STATE.md --confidence high ;;
    V1) run index; run read wiki/hermes.md; run read wiki/wiki-search.md
        run answer S2 "The wiki search service needs hermes, and its index (rebuilt by a timer on hermes at 02:30) goes stale." --pages hermes.md,wiki-search.md --confidence high ;;
    V2) run search hermes needs; run read wiki/wiki-search.md
        run answer S2 "The wiki search service needs hermes; when hermes is down the index goes stale." --pages wiki-search.md --confidence high ;;
    V3) run vsearch what depends on hermes; run read wiki/hermes.md
        run answer S2 "The wiki search service (qmd) needs hermes; the index goes stale when hermes is down." --pages hermes.md --confidence high ;;
    V4) run query what stops if hermes goes down; run read wiki/hermes.md
        run answer S2 "The wiki search service (qmd) needs hermes; the index goes stale when hermes is down." --pages hermes.md --confidence high ;;
    V5) run deps hermes; run deps wiki-search
        run answer S2 "Direct: the wiki search service (runs on hermes). Nothing else depends on wiki-search, so no second hop." --pages hermes.md,wiki-search.md --confidence high ;;
    V6) run depsview hermes
        run answer S2 "Direct: the wiki search service; no second-hop dependents." --pages hermes.md,wiki-search.md --confidence high ;;
    V7) run index; run read wiki/hermes.md; run grep 'depends_on:: \[\[hermes\]\]' wiki
        run answer S2 "The wiki search service needs hermes; its index goes stale when hermes is down." --pages hermes.md,wiki-search.md --confidence high ;;
  esac
  # ---- refusal probes (own question id so S1/S2 metrics stay clean) ----
  run start PROBE
  run read ../../etc/passwd
  run read raw/manual/denon-avr-x1700h-owners-manual.pdf
  run read wiki/does-not-exist.md
  case $v in
    V0) run index; run read wiki/atlas.md; run search x; run vsearch x; run query x; run deps atlas; run depsview atlas; run ls wiki; run grep atlas wiki ;;
    V1) run search x; run vsearch x; run query x; run grep atlas; run ls wiki; run deps atlas; run depsview atlas; run read raw/lab/LAB-STATE.md ;;
    V2) run vsearch x; run query x; run grep atlas; run ls wiki; run deps atlas; run read raw/lab/LAB-STATE.md ;;
    V3) run search x; run query x; run grep atlas; run deps atlas; run read raw/lab/LAB-STATE.md ;;
    V4) run search x; run vsearch x; run grep atlas; run deps atlas; run depsview atlas; run read deps/atlas.md ;;
    V5) run depsview atlas; run read deps/atlas.md; run grep atlas; run deps ../etc; run deps titan ;;   # deps titan must NOT list plex (stale edge under ## Superseded)
    V6) run grep atlas; run ls wiki; run search x; run read raw/lab/LAB-STATE.md; run depsview titan ;;
    V7) run search x; run vsearch x; run query x; run deps atlas; run depsview atlas; run read raw/lab/LAB-STATE.md; run ls raw; run grep atlas raw; run read deps/atlas.md; run grep 'depends_on:: \[\[titan\]\]' wiki ;;   # naive grep DOES show plex (stale); protocol tells the reader to drop it
  esac
  run answer PROBE "probe only" --pages "" --confidence low
  # ---- step cap probe (V1 only; a 9th call must be refused) ----
  if [ "$v" = V1 ]; then
    run start CAP
    for i in 1 2 3 4 5 6 7 8 9; do run read wiki/atlas.md 1-2; done
    run answer CAP "cap probe" --pages "" --confidence low
  fi
  metrics.py "$MM_RUN" > /dev/null
done
echo "transcript: $OUT"
