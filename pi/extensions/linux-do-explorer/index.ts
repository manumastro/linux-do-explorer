import type { ExtensionAPI } from "@mariozechner/pi-coding-agent";
import { execSync } from "node:child_process";
import * as fs from "node:fs";
import * as path from "node:path";
import { fileURLToPath } from "node:url";

const EXT_DIR = path.dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = path.resolve(EXT_DIR, "../../..");
const MANIFEST_PATH = path.join(REPO_ROOT, "pi", "manifest.json");

type Manifest = {
  guides?: Array<{ id: string; file: string; role: string }>;
  smokeTests?: Array<{ label: string; cmd: string }>;
  bootstrapOrder?: string[];
  defaults?: Record<string, unknown>;
};

function readManifest(): Manifest | null {
  try {
    return JSON.parse(fs.readFileSync(MANIFEST_PATH, "utf8")) as Manifest;
  } catch {
    return null;
  }
}

function guideExists(rel: string): boolean {
  return fs.existsSync(path.join(REPO_ROOT, rel));
}

function runShell(cmd: string): { ok: boolean; output: string } {
  try {
    const output = execSync(cmd, {
      encoding: "utf8",
      timeout: 120_000,
      stdio: ["ignore", "pipe", "pipe"],
    });
    return { ok: true, output: output.trim() };
  } catch (err) {
    const e = err as { stdout?: string; stderr?: string; message?: string };
    const output = [e.stdout, e.stderr, e.message].filter(Boolean).join("\n").trim();
    return { ok: false, output };
  }
}

export default function linuxDoExplorer(pi: ExtensionAPI) {
  pi.registerCommand("explorer-guide", {
    description: "Elenco guide linux-do-explorer e percorsi repo",
    handler: async (_args, ctx) => {
      const manifest = readManifest();
      const lines = [
        `linux-do-explorer: ${REPO_ROOT}`,
        "",
        "Guide principali:",
      ];

      if (manifest?.guides) {
        for (const g of manifest.guides) {
          const mark = guideExists(g.file) ? "✓" : "✗";
          lines.push(`  ${mark} ${g.file} — ${g.role}`);
        }
      } else {
        lines.push("  (manifest non trovato)");
      }

      lines.push(
        "",
        "Skills: /skill:vps-stack-relay · /skill:relay-explorer",
        "Altri comandi: /stack-bootstrap · /relay-test [provider] [model]",
        "",
        "Sorgente di verità stack: VPS-STACK-RELAY.md (decrypt da ENCRYPTED)",
      );

      ctx.ui.notify(lines.join("\n"), "info");
    },
  });

  pi.registerCommand("stack-bootstrap", {
    description: "Checklist per riprodurre lo stack Pi su un nuovo ambiente",
    handler: async (_args, ctx) => {
      const manifest = readManifest();
      const lines = [
        "Bootstrap stack (linux-do-explorer + my-pi)",
        "",
        `Repo: ${REPO_ROOT}`,
        "",
      ];

      if (manifest?.bootstrapOrder) {
        manifest.bootstrapOrder.forEach((step, i) => {
          lines.push(`${i + 1}. ${step}`);
        });
      }

      lines.push(
        "",
        "Script automatico:",
        `  bash ${path.join(REPO_ROOT, "scripts", "bootstrap-pi.sh")}`,
        "",
        "Segreti: bash scripts/sync-pi-secrets.sh import",
        "(o rsync stack-backup/ dal VPS sorgente, o §13 VPS-STACK-RELAY.md).",
      );

      ctx.ui.notify(lines.join("\n"), "info");
    },
  });

  pi.registerCommand("relay-test", {
    description: "Smoke test provider Pi (default: stack attuale)",
    getArgumentCompletions: (prefix) => {
      const providers = [
        "claude-anyrouter",
        "mimo-cn",
        "openai-anbalu",
        "claude-routerpark",
        "grok2api-local",
        "deepseek",
      ];
      return providers
        .filter((p) => p.startsWith(prefix.toLowerCase()))
        .map((p) => ({ label: p, value: p }));
    },
    handler: async (args, ctx) => {
      const parts = args.trim().split(/\s+/).filter(Boolean);
      let cmd: string;

      if (parts.length === 0) {
        cmd = "pi --print ok";
      } else if (parts.length === 1) {
        cmd = `pi --provider ${parts[0]} --print ok`;
      } else {
        cmd = `pi --provider ${parts[0]} --model ${parts[1]} --print ok`;
      }

      ctx.ui.notify(`Running: ${cmd}`, "info");
      const result = runShell(cmd);
      ctx.ui.notify(
        result.ok ? `OK\n${result.output.slice(0, 500)}` : `FAIL\n${result.output.slice(0, 800)}`,
        result.ok ? "info" : "error",
      );
    },
  });
}