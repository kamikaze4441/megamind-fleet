#!/usr/bin/env python3
# Fetches the benchmark corpus into $B/raw/<group>/ ; HTML -> main-content extraction (html.parser) -> pandoc gfm.
import subprocess, sys, os, json, datetime, re
from html.parser import HTMLParser

B = "/workspace/megamind-fleet/run1/03-benchmark"
UA = "Mozilla/5.0 (X11; Linux x86_64) megamind-bench/1.0"

SOURCES = [
 # id, group, filename, url, kind
 ("unraid-array","unraid","array-overview.md","https://docs.unraid.net/unraid-os/using-unraid-to/manage-storage/array/overview/","html"),
 ("unraid-cache-pools","unraid","cache-pools.md","https://docs.unraid.net/unraid-os/using-unraid-to/manage-storage/cache-pools/","html"),
 ("unraid-zfs","unraid","zfs-storage.md","https://docs.unraid.net/unraid-os/advanced-configurations/optimize-storage/zfs-storage/","html"),
 ("unraid-shares","unraid","shares.md","https://docs.unraid.net/unraid-os/using-unraid-to/manage-storage/shares/","html"),
 ("unraid-docker","unraid","docker-managing-containers.md","https://docs.unraid.net/unraid-os/using-unraid-to/run-docker-containers/managing-and-customizing-containers/","html"),
 ("unraid-vm-setup","unraid","vm-setup.md","https://docs.unraid.net/unraid-os/using-unraid-to/create-virtual-machines/vm-setup/","html"),
 ("unraid-tailscale","unraid","tailscale.md","https://docs.unraid.net/unraid-os/system-administration/secure-your-server/tailscale/","html"),
 ("unraid-settings","unraid","customize-settings-notifications-ups.md","https://docs.unraid.net/unraid-os/getting-started/set-up-unraid/customize-unraid-settings/","html"),
 ("ollama-api","ollama","api.md","https://docs.ollama.com/api.md","md"),
 ("ollama-modelfile","ollama","modelfile.md","https://docs.ollama.com/modelfile.md","md"),
 ("ollama-gpu","ollama","gpu.md","https://docs.ollama.com/gpu.md","md"),
 ("ollama-faq","ollama","faq.md","https://docs.ollama.com/faq.md","md"),
 ("ollama-docker","ollama","docker.md","https://docs.ollama.com/docker.md","md"),
 ("ollama-openai","ollama","openai-compatibility.md","https://docs.ollama.com/api/openai-compatibility.md","md"),
 ("syncthing-getting-started","syncthing","getting-started.md","https://docs.syncthing.net/intro/getting-started.html","html"),
 ("syncthing-foldertypes","syncthing","foldertypes.md","https://docs.syncthing.net/users/foldertypes.html","html"),
 ("syncthing-versioning","syncthing","versioning.md","https://docs.syncthing.net/users/versioning.html","html"),
 ("syncthing-ignoring","syncthing","ignoring.md","https://docs.syncthing.net/users/ignoring.html","html"),
 ("syncthing-firewall","syncthing","firewall.md","https://docs.syncthing.net/users/firewall.html","html"),
 ("tailscale-exit-nodes","tailscale","exit-nodes.md","https://tailscale.com/docs/features/exit-nodes.md","md"),
 ("tailscale-subnet-routers","tailscale","subnet-routers.md","https://tailscale.com/docs/features/subnet-routers.md","md"),
 ("tailscale-acls","tailscale","acls.md","https://tailscale.com/docs/features/access-control/acls.md","md"),
 ("tailscale-magicdns","tailscale","magicdns.md","https://tailscale.com/docs/features/magicdns.md","md"),
 ("tailscale-ssh","tailscale","tailscale-ssh.md","https://tailscale.com/docs/features/tailscale-ssh.md","md"),
 ("tailscale-unraid","tailscale","unraid.md","https://tailscale.com/docs/integrations/unraid.md","md"),
 ("cc-settings","claude-code","settings.md","https://code.claude.com/docs/en/settings.md","md"),
 ("cc-permissions","claude-code","permissions.md","https://code.claude.com/docs/en/permissions.md","md"),
 ("cc-hooks","claude-code","hooks.md","https://code.claude.com/docs/en/hooks.md","md"),
 ("cc-skills","claude-code","skills.md","https://code.claude.com/docs/en/skills.md","md"),
 ("cc-sub-agents","claude-code","sub-agents.md","https://code.claude.com/docs/en/sub-agents.md","md"),
 ("cc-memory","claude-code","memory.md","https://code.claude.com/docs/en/memory.md","md"),
 ("cc-mcp","claude-code","mcp.md","https://code.claude.com/docs/en/mcp.md","md"),
 ("cc-sandboxing","claude-code","sandboxing.md","https://code.claude.com/docs/en/sandboxing.md","md"),
]

class Extract(HTMLParser):
    """Collects the raw HTML of the first element matching a predicate (article / role=main)."""
    VOID = {"area","base","br","col","embed","hr","img","input","link","meta","param","source","track","wbr"}
    def __init__(self, pred):
        super().__init__(convert_charrefs=False)
        self.pred, self.depth, self.out, self.done = pred, 0, [], False
    def handle_starttag(self, tag, attrs):
        if self.done: return
        if self.depth == 0:
            if self.pred(tag, dict(attrs)):
                self.depth = 1; self.out.append(self.get_starttag_text())
            return
        self.out.append(self.get_starttag_text())
        if tag not in self.VOID: self.depth += 1
    def handle_startendtag(self, tag, attrs):
        if self.depth and not self.done: self.out.append(self.get_starttag_text())
    def handle_endtag(self, tag):
        if self.depth == 0 or self.done: return
        if tag in self.VOID: return
        self.out.append(f"</{tag}>"); self.depth -= 1
        if self.depth == 0: self.done = True
    def handle_data(self, d):
        if self.depth and not self.done: self.out.append(d)
    def handle_entityref(self, n):
        if self.depth and not self.done: self.out.append(f"&{n};")
    def handle_charref(self, n):
        if self.depth and not self.done: self.out.append(f"&#{n};")

def pred_for(url):
    if "syncthing" in url:
        return lambda t, a: t == "div" and a.get("role") == "main"
    return lambda t, a: t == "article"

def curl(url):
    r = subprocess.run(["curl","-sSL","-A",UA,"--max-time","60","-w","\n%{http_code} %{url_effective}",url],capture_output=True)
    body, _, tail = r.stdout.rpartition(b"\n")
    code, eff = tail.decode().split(" ",1)
    return body, int(code), eff

def main():
    today = datetime.date.today().isoformat()
    log = []
    for sid, group, fn, url, kind in SOURCES:
        os.makedirs(f"{B}/raw/{group}", exist_ok=True)
        path = f"{B}/raw/{group}/{fn}"
        body, code, eff = curl(url)
        if code != 200:
            log.append(dict(id=sid, url=url, status=code, error="http")); print("FAIL", sid, code); continue
        if kind == "md":
            text = body.decode("utf-8", "replace")
        else:
            ex = Extract(pred_for(url)); ex.feed(body.decode("utf-8","replace"))
            frag = "".join(ex.out)
            frag = re.sub(r"<svg\b.*?</svg>", "", frag, flags=re.S)
            frag = re.sub(r"<img\b[^>]*src=\"data:[^\"]*\"[^>]*>", "", frag)
            if not frag:
                log.append(dict(id=sid, url=url, status=code, error="no main element")); print("FAIL extract", sid); continue
            p = subprocess.run(["pandoc","-f","html","-t","gfm-raw_html","--wrap=none"],input=frag.encode(),capture_output=True)
            text = p.stdout.decode()
            text = re.sub(r"\[[\u200b\u00b6]\]\(#[^)]*\)", "", text)
            text = re.sub(r"!\[([^\]]*)\]\(data:[^)]*\)", r"[image: \1]", text)
        # credential rule: drop anything shaped like a live key (docs examples included), and count it
        text, nred = re.subn(r"tskey-[a-z]+-[A-Za-z0-9]{6,}[A-Za-z0-9-]*", "tskey-[REDACTED-BY-BENCHMARK]", text)
        if nred: print("REDACTED", sid, nred)
        header = f"<!-- source: {url} | fetched: {today} | effective-url: {eff} -->\n\n"
        with open(path,"w") as f: f.write(header + text)
        log.append(dict(id=sid, group=group, redactions=nred, url=url, effective=eff, status=code, path=f"raw/{group}/{fn}", bytes=os.path.getsize(path), fetched=today))
        print("ok", sid, os.path.getsize(path))
    json.dump(log, open("/tmp/b1/fetch-log.json","w"), indent=1)

if __name__ == "__main__":
    main()
