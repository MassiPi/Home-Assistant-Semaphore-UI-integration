# Semaphore UI Home Assistant Integration

A Home Assistant custom integration for connecting and monitoring **Semaphore UI** directly from your smart home dashboard.

---

## 🚀 The problem

In my homelab, I deployed the magnificent **Semaphore UI** to automate and orchestrate security updates across all my servers.

It worked beautifully.

But there was one small annoyance.

The only way to check whether everything was actually running correctly was… to open Semaphore itself.

Every. Single. Time.

Not exactly the kind of observability experience you want when you're trying to keep things automated.

---

## 💡 The idea

At some point I asked myself:

> *“If Home Assistant is already the control center of my home… why isn’t it also the control center of my infrastructure?”*

And that was it.

This integration was born.

The goal is simple:

👉 Bring key information from the Semaphore UI into Home Assistant  
👉 Make server updates result visible alongside your home automation  
👉 Eliminate the need to constantly jump between dashboards  

Now your infrastructure health becomes part of your Home Assistant ecosystem.

---

## 🧩 What this integration does

- Connects Home Assistant to your Semaphore UI instance
- Authenticates using API tokens
- Validates connectivity and API availability
- Checks the last result of each template you set up
- Working through APIs, allows future expansion into basically everything Semaphore does.

---

## ⚙️ Installation (HACS)

1. Add this repository to HACS as a **custom repository**
2. Select **Integration**
3. Install "Semaphore UI"
4. Restart Home Assistant
5. Add integration via UI:
   - URL: your Semaphore instance (https://...)
   - API Token: generated from Semaphore UI
   - Project ID: target project

---

## 🔐 Requirements

- Home Assistant 2023+
- Semaphore UI instance reachable from HA
- Valid Semaphore API token

---

## 📦 Configuration

During setup you will need:

| Field       | Description |
|------------|-------------|
| URL        | Full Semaphore UI URL (https://...) |
| Token      | API token generated in Semaphore |
| Project ID | Target project identifier |

---

## 🧠 Design philosophy

This integration is intentionally lightweight.

It does not try to replace Semaphore UI.

Instead, it acts as a **bridge between infrastructure automation and home observability**.

Home Assistant becomes the single pane of glass — not just for your home, but for your homelab as well.

---

## ❤️ Why this exists

Because checking logs manually is boring.

Because automation should be visible.

Because your homelab deserves a dashboard that feels alive.

And because… i was bored.

---

## 🧑‍💻 Author

Built with curiosity and an heavy butt, thus refusing to keep switching tabs just to check if things are running.
And clearly not a programmer 🤣

---

## 📜 License

MIT — do whatever you want with this code, modify it, fork it, break it, improve it.

Just keep the original attribution and don’t quietly rewrite history by pretending you wrote it from scratch. Forks are fine — serial rebranding without credit is not the vibe and to me is explicitly what a community should not do.

If you want to add improvements, features, or fixes, even better: open a pull request instead of silently fragmenting the ecosystem.
