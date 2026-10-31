import * as React from "react"
import { addPropertyControls, ControlType } from "framer"

// Replace these defaults by downloading this component from a customized object.
const savedScene: any = /* THREED_SCENE */ {"id":"rangefinder-camera","label":"Studio camera","state":{"background":"#ebe9e2","explodeStrength":0.85},"colors":{"body":"#e8e4d8","secondary":"#a2b1dc","accent":"#3054d7"},"materials":[],"view":{"yaw":0,"pitch":0},"theme":"light","transparent":true,"motion":"hover"} /* END_SCENE */
const savedLibrary = /* THREED_LIBRARY */ "" /* END_LIBRARY */

function hex(value: string, fallback: string) {
    if (/^#[\da-f]{6}$/i.test(value || "")) return value
    if (/^#[\da-f]{3}$/i.test(value || "")) return "#" + value.slice(1).split("").map(c => c + c).join("")
    const rgb = /^rgba?\(\s*([\d.]+)[,\s]+([\d.]+)[,\s]+([\d.]+)/i.exec(value || "")
    return rgb ? "#" + rgb.slice(1, 4).map(n => Math.max(0, Math.min(255, Math.round(Number(n)))).toString(16).padStart(2, "0")).join("") : fallback
}

/**
 * @framerSupportedLayoutWidth any
 * @framerSupportedLayoutHeight any
 * @framerIntrinsicWidth 400
 * @framerIntrinsicHeight 400
 */
export default function Threed(props: any) {
    const { library = savedLibrary, object = savedScene.id, theme = savedScene.theme, transparent = true, background = savedScene.state.background, motion = savedScene.motion, amount = savedScene.state.explodeStrength, follow = true, turntable = false, body, secondary, accent, light = 3, shadow = 0.55, style } = props
    let src = ""
    try {
        const base = new URL(library)
        if (!["https:", "http:"].includes(base.protocol) || base.username || base.password) throw Error()
        base.hash = ""; base.search = ""
        if (!base.pathname.endsWith("/")) base.pathname += "/"
        const scene = { ...savedScene, id: object, theme, transparent, motion, colors: { ...savedScene.colors }, state: { ...savedScene.state, background: hex(background, theme === "dark" ? "#28302d" : "#ebe9e2"), intensity: light, shadow, explodeStrength: amount, follow, spin: turntable } }
        for (const [slot, color] of Object.entries({ body, secondary, accent })) if (color) scene.colors[slot] = hex(String(color), "#e8e4d8")
        const url = new URL("embed.html", base)
        url.hash = new URLSearchParams({ scene: JSON.stringify(scene) }).toString()
        src = url.href
    } catch {}
    return src ? React.createElement("iframe", {
        title: `${object} — threed®`, src, loading: "lazy",
        style: { ...style, display: "block", width: "100%", height: "100%", border: 0, background: "transparent" },
    }) : React.createElement("div", {
        style: { ...style, width: "100%", height: "100%", display: "grid", placeItems: "center", padding: 24, boxSizing: "border-box", background: "#ebe9e2", color: "#29332d", font: "14px/1.5 sans-serif", textAlign: "center" },
    }, "Set Library URL to your published threed® library address.")
}

Threed.defaultProps = { library: savedLibrary, object: savedScene.id, theme: savedScene.theme, transparent: savedScene.transparent, motion: savedScene.motion, amount: savedScene.state.explodeStrength ?? 0.85, background: savedScene.state.background, light: savedScene.state.intensity ?? 3, shadow: savedScene.state.shadow ?? 0.55, follow: savedScene.state.follow ?? true, turntable: savedScene.state.spin ?? false, width: 400, height: 400 }
addPropertyControls(Threed, {
    library: { type: ControlType.String, title: "Library URL", defaultValue: savedLibrary, description: "Use your published HTTPS library URL. Localhost is for local preview only." },
    object: { type: ControlType.String, title: "Object ID", defaultValue: savedScene.id },
    body: { type: ControlType.Color, title: "Body", optional: true },
    secondary: { type: ControlType.Color, title: "Secondary", optional: true },
    accent: { type: ControlType.Color, title: "Accent", optional: true },
    theme: { type: ControlType.Enum, title: "Theme", options: ["light", "dark"], optionTitles: ["Light", "Dark"], defaultValue: savedScene.theme, displaySegmentedControl: true },
    transparent: { type: ControlType.Boolean, title: "Transparent", defaultValue: savedScene.transparent },
    background: { type: ControlType.Color, title: "Background", hidden: (p: any) => p.transparent },
    motion: { type: ControlType.Enum, title: "Motion", options: ["still", "hover", "loop"], optionTitles: ["Still", "Hover", "Loop"], defaultValue: savedScene.motion, displaySegmentedControl: true },
    amount: { type: ControlType.Number, title: "Amount", min: 0, max: 1.5, step: 0.05, defaultValue: savedScene.state.explodeStrength ?? 0.85, hidden: (p: any) => p.motion === "still" },
    follow: { type: ControlType.Boolean, title: "Mouse follow", defaultValue: savedScene.state.follow ?? true },
    turntable: { type: ControlType.Boolean, title: "Turntable", defaultValue: savedScene.state.spin ?? false },
    light: { type: ControlType.Number, title: "Light", min: 0, max: 7, step: 0.1, defaultValue: savedScene.state.intensity ?? 3 },
    shadow: { type: ControlType.Number, title: "Shadow", min: 0, max: 1, step: 0.05, defaultValue: savedScene.state.shadow ?? 0.55 },
})
