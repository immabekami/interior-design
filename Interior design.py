import json
from datetime import datetime
from io import BytesIO

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="RoomMuse | Interior Design Studio",
    page_icon="🪴",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------- Design catalogue -----------------------------
STYLES = {
    "Minimalist": {
        "description": "Calm, uncluttered spaces with purposeful furniture and a restrained palette.",
        "palette": ["#F4F1EA", "#D9D3C7", "#A7A99A", "#5F6658", "#2F332E"],
        "walls": "Warm white or soft greige",
        "flooring": "Pale oak, light tile, or polished concrete",
        "curtains": "Plain linen in ivory or sand",
        "lighting": "Simple layered lighting with warm-white bulbs",
        "decor": "A few carefully chosen objects, one plant, and simple artwork",
        "furniture": "Low-profile furniture with clean lines and hidden storage",
        "layout": "Keep clear walking paths and leave breathing room around each key piece.",
        "why": "The restrained palette and limited visual clutter support a calm, functional room.",
        "image_query": "minimalist interior design room neutral",
    },
    "Modern": {
        "description": "Clean silhouettes, practical materials, and a balanced mix of textures.",
        "palette": ["#F5F3EF", "#C8C9C6", "#8D9698", "#344B50", "#20282A"],
        "walls": "Soft white with one muted accent wall",
        "flooring": "Wood-look flooring, stone-look tile, or smooth concrete",
        "curtains": "Full-length neutral curtains with a simple track",
        "lighting": "Recessed or track lighting plus a statement pendant",
        "decor": "Abstract art, sculptural accessories, and a large plant",
        "furniture": "Streamlined pieces with metal, wood, or glass details",
        "layout": "Anchor the room with one focal point, then arrange seating or work areas around it.",
        "why": "Simple forms and mixed materials create a contemporary look without overcrowding the room.",
        "image_query": "modern interior design room",
    },
    "Contemporary": {
        "description": "Current, comfortable design with soft shapes and thoughtfully mixed finishes.",
        "palette": ["#F7F4EF", "#D8CFC4", "#A6B0AA", "#6B7D78", "#3C4744"],
        "walls": "Cream, warm white, or a muted green-grey",
        "flooring": "Natural wood tones or large-format neutral tiles",
        "curtains": "Textured linen or a subtle tone-on-tone fabric",
        "lighting": "Layered ambient lighting and one sculptural feature",
        "decor": "Large-scale art, rounded accessories, and textured cushions",
        "furniture": "Comfortable pieces with a mix of rounded and straight forms",
        "layout": "Create a clear focal area and balance larger pieces with open space.",
        "why": "A mix of current shapes and tactile materials feels fresh but remains adaptable.",
        "image_query": "contemporary interior design room",
    },
    "Scandinavian": {
        "description": "Bright, practical rooms with natural wood, soft textiles, and simple forms.",
        "palette": ["#FAF8F2", "#E5DCCB", "#C4D0C4", "#8D9C8A", "#414B43"],
        "walls": "White, pale beige, or very light sage",
        "flooring": "Light natural wood or a pale wood-look finish",
        "curtains": "Sheer white or light beige linen",
        "lighting": "Warm ambient lamps with simple shades",
        "decor": "Plants, woven baskets, cosy throws, and minimal artwork",
        "furniture": "Light wood, simple silhouettes, and useful storage",
        "layout": "Keep the room bright and open; use baskets and compact furniture to control clutter.",
        "why": "Light colours, natural textures, and practical pieces make the room feel welcoming.",
        "image_query": "Scandinavian interior design room",
    },
    "Industrial": {
        "description": "Honest materials, dark accents, exposed-looking finishes, and utilitarian details.",
        "palette": ["#E9E4DC", "#B7B0A5", "#73716C", "#41484A", "#242A2B"],
        "walls": "Warm grey, off-white, or a restrained concrete-look feature",
        "flooring": "Concrete-look tile, dark wood, or durable neutral flooring",
        "curtains": "Charcoal, taupe, or simple woven neutrals",
        "lighting": "Black metal pendants, wall lights, and task lamps",
        "decor": "Graphic art, metal shelving, and a few textured accessories",
        "furniture": "Wood and metal combinations with sturdy, simple forms",
        "layout": "Use one strong focal point and soften harder materials with rugs and textiles.",
        "why": "Metal details and robust finishes deliver an industrial feel while textiles add comfort.",
        "image_query": "industrial interior design room",
    },
    "Bohemian": {
        "description": "Layered textiles, natural materials, plants, and expressive personal objects.",
        "palette": ["#F5E9D7", "#D7B99A", "#B77B55", "#687A58", "#573D32"],
        "walls": "Cream, warm white, or a muted clay tone",
        "flooring": "Natural wood or neutral tile layered with rugs",
        "curtains": "Cotton or linen in earthy tones",
        "lighting": "Warm lamps, woven pendants, and gentle accent lighting",
        "decor": "Plants, patterned cushions, woven baskets, and collected artwork",
        "furniture": "Comfortable wood or rattan pieces with varied textures",
        "layout": "Layer rugs and textiles, but keep doorways and main walking routes clear.",
        "why": "Layered materials and personal accessories create a relaxed, individual space.",
        "image_query": "bohemian interior design room",
    },
    "Vintage": {
        "description": "Characterful pieces, nostalgic details, and a considered mix of old and new.",
        "palette": ["#F2E8D9", "#C8B49A", "#A76E59", "#68765B", "#403A36"],
        "walls": "Cream, muted olive, dusty rose, or a soft heritage colour",
        "flooring": "Wood tones or classic patterned tile",
        "curtains": "Textured fabric or a subtle traditional pattern",
        "lighting": "Warm table lamps and a vintage-inspired pendant",
        "decor": "Framed prints, second-hand finds, ceramics, and a mirror",
        "furniture": "One or two character pieces balanced with practical modern items",
        "layout": "Give standout vintage pieces space and avoid making every item compete for attention.",
        "why": "A blend of character pieces and simpler essentials feels collected rather than cluttered.",
        "image_query": "vintage interior design room",
    },
    "Traditional": {
        "description": "Timeless shapes, coordinated furnishings, symmetry, and classic decorative details.",
        "palette": ["#F5F0E6", "#D5C6AE", "#9B8064", "#58634F", "#3E3830"],
        "walls": "Warm cream, beige, or a soft heritage green",
        "flooring": "Wood, stone-look tile, or a classic neutral finish",
        "curtains": "Full-length lined curtains in a coordinated fabric",
        "lighting": "Warm lamps, wall sconces, and a classic central fixture",
        "decor": "Framed art, ceramics, a mirror, and coordinated cushions",
        "furniture": "Classic profiles with comfortable upholstery and useful storage",
        "layout": "Use symmetry where practical and maintain clear paths through the room.",
        "why": "Balanced arrangements and classic details give the room a timeless, cohesive character.",
        "image_query": "traditional interior design room",
    },
    "Luxury": {
        "description": "A polished look built from thoughtful lighting, tactile finishes, and a few focal pieces.",
        "palette": ["#F5F0E7", "#C9B99F", "#9B8668", "#3F5550", "#242B29"],
        "walls": "Warm neutral paint with one carefully chosen feature finish",
        "flooring": "Quality wood-look flooring, stone-look tile, or a large neutral rug",
        "curtains": "Full-height, well-finished curtains in a rich neutral",
        "lighting": "Layered lighting with a statement pendant and table lamps",
        "decor": "Large artwork, a sculptural vase, and coordinated soft furnishings",
        "furniture": "Comfortable statement pieces with refined finishes",
        "layout": "Prioritise proportion, symmetry, and uncluttered surfaces over the number of objects.",
        "why": "A restrained palette and a few high-impact details create a refined atmosphere.",
        "image_query": "luxury interior design room elegant",
    },
    "Rustic": {
        "description": "Natural textures, warm earthy colours, and sturdy pieces with a relaxed feel.",
        "palette": ["#F1E8D9", "#C8B397", "#9A795B", "#72795B", "#493B30"],
        "walls": "Warm white, sand, or muted earthy tones",
        "flooring": "Natural wood tones or textured neutral tile",
        "curtains": "Linen or cotton in cream, tan, or olive",
        "lighting": "Warm light with wood, ceramic, or woven shades",
        "decor": "Woven baskets, handmade ceramics, plants, and textured rugs",
        "furniture": "Solid-looking wood, simple upholstery, and practical storage",
        "layout": "Group furniture for comfort and balance rustic textures with easy-to-clean surfaces.",
        "why": "Earthy colours and natural-looking materials make the room feel grounded and inviting.",
        "image_query": "rustic interior design room",
    },
    "Minimalist African-inspired": {
        "description": "A contemporary, uncluttered space featuring earthy tones, natural materials, and locally inspired craft.",
        "palette": ["#F4E8D5", "#D5B995", "#B96E45", "#59664A", "#3B332B"],
        "walls": "Warm white, sand, or a restrained clay accent",
        "flooring": "Warm wood tones, terrazzo-look surfaces, or neutral tile",
        "curtains": "Cotton or linen in cream, ochre, or muted earth tones",
        "lighting": "Warm layered lighting with woven or ceramic details",
        "decor": "Handcrafted baskets, locally made art, natural fibres, and a few plants",
        "furniture": "Simple wood furniture with woven or handcrafted accents",
        "layout": "Keep the base simple and let a few meaningful handmade pieces become focal points.",
        "why": "Natural textures and thoughtful craft references create warmth without visual overload.",
        "image_query": "contemporary African inspired interior design",
    },
    "Academia": {
        "description": "Bookish, layered spaces with rich wood, deep colours, reading light, and collected objects.",
        "palette": ["#F0E7D7", "#B9A17D", "#6F7659", "#654A3A", "#302D2A"],
        "walls": "Cream, olive, muted brown, or a deep accent wall",
        "flooring": "Wood tones with a patterned or textured rug",
        "curtains": "Heavy cotton or linen in olive, brown, or cream",
        "lighting": "A desk lamp, warm floor lamp, and soft ambient light",
        "decor": "Books, framed prints, a pinboard, ceramics, and plants",
        "furniture": "Wooden desk or shelving, a comfortable reading chair, and storage",
        "layout": "Create a distinct reading or study zone and keep task lighting close to the work surface.",
        "why": "Books, warm light, and layered textures support a cosy, thoughtful atmosphere.",
        "image_query": "dark academia interior design room",
    },
    "Y2K": {
        "description": "Playful early-2000s-inspired colour, glossy accents, curves, and expressive accessories.",
        "palette": ["#FFF2F8", "#F5B7D2", "#B7D5F7", "#A6B7E8", "#56466D"],
        "walls": "White or pale pink with a removable accent treatment",
        "flooring": "Light neutral flooring with a colourful rug",
        "curtains": "White, pastel, or a simple iridescent-inspired accent",
        "lighting": "Colour-changing accent lights plus practical warm-white lighting",
        "decor": "Curved mirrors, playful art, colourful cushions, and translucent accessories",
        "furniture": "Compact pieces with rounded forms and glossy or colourful details",
        "layout": "Keep the main furniture functional and use accessories for the bolder Y2K look.",
        "why": "Pastel colours and playful accents create the aesthetic without sacrificing everyday use.",
        "image_query": "Y2K inspired bedroom interior design",
    },
    "Soft girl": {
        "description": "Gentle pastels, cosy fabrics, rounded details, and a light, playful atmosphere.",
        "palette": ["#FFF7F5", "#F6DCE7", "#E9C6D5", "#C8D8C4", "#8D9E9A"],
        "walls": "Warm white, blush, or pale lavender",
        "flooring": "Light wood or a neutral floor with a soft rug",
        "curtains": "Sheer white or pale pastel fabric",
        "lighting": "Warm bedside lamps and soft diffused lighting",
        "decor": "Soft cushions, small prints, flowers, and rounded mirrors",
        "furniture": "Light-coloured, comfortable furniture with gentle shapes",
        "layout": "Use a calm base and repeat two or three pastel colours for cohesion.",
        "why": "Soft colours and tactile fabrics make the space feel gentle and coordinated.",
        "image_query": "soft girl aesthetic bedroom interior",
    },
    "Maximalist": {
        "description": "Expressive colour, layered patterns, collected art, and confident combinations.",
        "palette": ["#F7E9D7", "#D95F59", "#E3B84D", "#477C69", "#49365E"],
        "walls": "A warm neutral or a bold colour chosen to support the room's palette",
        "flooring": "A simple durable base with patterned rugs if desired",
        "curtains": "A rich colour or a pattern that repeats elsewhere in the room",
        "lighting": "Layered lamps and a distinctive statement fixture",
        "decor": "Gallery wall, patterned cushions, colourful ceramics, and plants",
        "furniture": "Mix shapes and eras while keeping scale and comfort in mind",
        "layout": "Choose a colour story first, then repeat colours across art, textiles, and accessories.",
        "why": "Repeating colours and balancing large and small patterns makes expressive design feel intentional.",
        "image_query": "maximalist colourful interior design room",
    },
}

ROOMS = [
    "Bedroom", "Living room", "Kitchen", "Bathroom", "Study room",
    "Dining room", "Play room", "Lounge", "Reception", "Gaming room",
]
FUNCTIONS = [
    "Storage", "Relaxation", "Studying or working", "Entertaining guests",
    "Maximising available space", "Family-friendly use", "Gaming or media",
    "Easy cleaning and maintenance",
]
COLOURS = [
    "Neutrals", "White", "Black", "Beige", "Brown", "Green", "Blue",
    "Pink", "Purple", "Red", "Yellow", "Orange", "Earth tones",
]
FURNITURE = [
    "Modern", "Classic", "Space-saving", "Multifunctional", "Luxury",
    "Second-hand or upcycled", "Locally made",
]
LIGHTING = [
    "Natural lighting", "Warm lighting", "Cool lighting", "Layered lighting",
    "Task lighting", "Colour-changing accent lighting",
]
MATERIALS = [
    "Wood", "Glass", "Metal", "Marble or stone-look", "Cotton", "Linen",
    "Rattan or woven fibres", "Ceramic", "Easy-clean synthetic fabrics",
]
BUDGET_LEVELS = ["Low", "Medium", "High"]
CURRENCY_OPTIONS = ["NGN (₦)", "USD ($)", "GBP (£)", "EUR (€)"]
CURRENCY_SYMBOL = {"NGN (₦)": "₦", "USD ($)": "$", "GBP (£)": "£", "EUR (€)": "€"}

# ----------------------------- Recommendation logic -----------------------------
def get_palette(style_name, preferred_colours):
    palette = STYLES[style_name]["palette"].copy()
    requested = set(preferred_colours or [])
    accent_map = {
        "White": "#FFFFFF", "Black": "#242424", "Beige": "#DCCBB2",
        "Brown": "#795548", "Green": "#6E8B68", "Blue": "#638BB5",
        "Pink": "#E7AFC1", "Purple": "#9A83B8", "Red": "#B94A48",
        "Yellow": "#E5C45B", "Orange": "#D98A4E", "Earth tones": "#B77B55",
        "Neutrals": "#B8B1A5",
    }
    for colour in requested:
        if colour in accent_map:
            palette[-2] = accent_map[colour]
            break
    return palette

def recommend_design(prefs):
    style_name = prefs["style"]
    style = STYLES[style_name]
    size = prefs["room_size"]
    budget = prefs["budget_level"]
    room = prefs["room_type"]
    functions = prefs["functions"]
    furniture_prefs = prefs["furniture"]
    light_prefs = prefs["lighting"]
    materials = prefs["materials"]
    palette = get_palette(style_name, prefs["colours"])

    if size == "Small":
        furniture = "Choose compact, appropriately scaled furniture; prioritise pieces with built-in storage."
        layout = "Place the largest piece against a suitable wall, keep the main walkway clear, and use vertical storage. Measure door swings and furniture before buying."
        space_tip = "Use wall shelves, under-bed or closed storage, mirrors where helpful, and furniture that serves more than one purpose."
    elif size == "Large":
        furniture = "Use a few well-proportioned anchor pieces and add secondary seating or storage only where useful."
        layout = "Create clear zones for the room's main activities, use rugs to define them, and balance large furniture with lighting and artwork."
        space_tip = "Divide the room into practical zones rather than filling every empty area."
    else:
        furniture = "Choose furniture that fits the room's proportions and leaves comfortable walking routes."
        layout = "Anchor the room with its main activity, then arrange supporting pieces around it while preserving circulation."
        space_tip = "Use closed storage for everyday items and reserve open surfaces for a few decorative objects."

    if "Space-saving" in furniture_prefs or "Multifunctional" in furniture_prefs or "Maximising available space" in functions:
        space_tip += " Prioritise nesting tables, storage ottomans, foldable pieces, or a desk with shelves where appropriate."
    if "Storage" in functions:
        furniture += " Include closed storage or baskets to keep frequently used items organised."
    if "Studying or working" in functions:
        light_note = "Add a task lamp and position the work surface near daylight when practical."
    elif "Gaming or media" in functions or room == "Gaming room":
        light_note = "Combine adjustable ambient lighting with glare-controlled task lighting and a tidy cable plan."
    else:
        light_note = "Use at least two lighting layers, such as general light plus a floor, table, or task lamp."

    lighting = style["lighting"]
    if "Warm lighting" in light_prefs:
        lighting += " Use warm-white bulbs for a cosy atmosphere."
    if "Cool lighting" in light_prefs:
        lighting += " Use neutral/cool task lighting only where clear visibility is important."
    if "Natural lighting" in light_prefs:
        lighting += " Keep window areas open where possible and use light-filtering window treatments."
    if "Task lighting" in light_prefs:
        lighting += " Include a focused task lamp for reading, studying, or detailed work."
    lighting += " " + light_note

    furniture_line = style["furniture"]
    if "Space-saving" in furniture_prefs or "Multifunctional" in furniture_prefs:
        furniture_line += " Favour nesting, foldable, stackable, or dual-purpose pieces."
    if "Second-hand or upcycled" in furniture_prefs:
        furniture_line += " Consider pre-loved furniture and refresh it with repair, paint, or new hardware."
    if "Locally made" in furniture_prefs:
        furniture_line += " Check local craftspeople and makers for suitable, repairable pieces."
    if "Luxury" in furniture_prefs and budget == "Low":
        furniture_line += " To keep costs manageable, use one statement item and choose affordable basics for the rest."

    if budget == "Low":
        budget_note = "Prioritise paint, layout, decluttering, second-hand finds, DIY artwork, and one or two high-impact accessories. Upgrade items gradually."
        cost_split = {"Furniture": 40, "Paint and wall finish": 20, "Lighting": 15, "Textiles": 15, "Decor and accessories": 10}
    elif budget == "Medium":
        budget_note = "Invest first in frequently used furniture, comfortable lighting, and durable textiles; save on decorative accessories."
        cost_split = {"Furniture": 45, "Paint and wall finish": 15, "Lighting": 15, "Textiles": 15, "Decor and accessories": 10}
    else:
        budget_note = "Spend selectively on durable anchor furniture, quality lighting, and tailored finishes. Compare quotes before committing."
        cost_split = {"Furniture": 45, "Paint and wall finish": 10, "Lighting": 20, "Textiles": 15, "Decor and accessories": 10}

    if prefs.get("custom_budget", 0) and prefs.get("custom_budget", 0) > 0:
        amount = float(prefs["custom_budget"])
        budget_rows = [{"Category": k, "Allocation (%)": v, "Estimated amount": amount * v / 100} for k, v in cost_split.items()]
        budget_df = pd.DataFrame(budget_rows)
    else:
        budget_df = pd.DataFrame([{"Category": k, "Allocation (%)": v, "Estimated amount": None} for k, v in cost_split.items()])

    if room == "Bedroom":
        decor = style["decor"] + "; consider bedside storage, comfortable bedding, and blackout or light-filtering curtains as needed."
        key_items = ["Bed and mattress", "Bedside lighting", "Bedding and pillows", "Clothing storage", "Curtains or blinds", "Rug (optional)", "Artwork or personal decor"]
    elif room in ["Living room", "Lounge", "Reception"]:
        decor = style["decor"] + "; add comfortable seating, a side table, and a durable rug if suitable."
        key_items = ["Main seating", "Coffee or side table", "Layered lighting", "Curtains or blinds", "Rug (optional)", "Artwork or focal decor", "Storage for everyday items"]
    elif room == "Kitchen":
        decor = style["decor"] + "; keep worktops easy to clean and prioritise safe, practical task lighting."
        key_items = ["Work surface organisation", "Task lighting", "Easy-clean storage", "Curtains or blinds suitable for the space", "Durable flooring", "Waste and recycling solution", "Small decorative accent"]
    elif room == "Bathroom":
        decor = style["decor"] + "; choose moisture-appropriate finishes and ensure lighting and ventilation suit the room."
        key_items = ["Mirror", "Moisture-suitable lighting", "Towel storage", "Bath mat", "Easy-clean accessories", "Ventilation check", "Moisture-appropriate finishes"]
    elif room == "Study room":
        decor = style["decor"] + "; keep the desk clear and combine task lighting with comfortable storage."
        key_items = ["Desk", "Supportive chair", "Task lamp", "Bookshelf or storage", "Cable management", "Curtains or blinds", "Pinboard or artwork"]
    elif room == "Dining room":
        decor = style["decor"] + "; centre the layout on a table with enough room to pull chairs out safely."
        key_items = ["Dining table", "Chairs", "Pendant or layered lighting", "Storage or serving surface", "Curtains or blinds", "Easy-clean rug (optional)", "Centrepiece"]
    elif room == "Play room":
        decor = style["decor"] + "; use accessible storage, wipeable finishes, and age-appropriate furnishings."
        key_items = ["Accessible toy storage", "Soft play rug or mat", "Book display", "Comfortable seating", "Task and ambient lighting", "Wipeable surfaces", "Age-appropriate decor"]
    elif room == "Gaming room":
        decor = style["decor"] + "; plan ventilation, cable management, comfortable seating, and screen glare control."
        key_items = ["Desk or gaming surface", "Comfortable chair", "Task lighting", "Ambient accent lighting", "Cable management", "Headset/controller storage", "Curtains or blinds"]
    else:
        decor = style["decor"] + "; keep circulation clear and choose durable finishes appropriate for the room's use."
        key_items = ["Main functional furniture", "Storage", "Suitable lighting", "Window treatment", "Durable flooring", "Artwork or decor", "Easy-clean accessories"]

    why = style["why"]
    if prefs["colours"]:
        why += f" The selected colour preferences ({', '.join(prefs['colours'])}) are reflected in the accent palette where possible."
    if materials:
        why += f" Consider incorporating {', '.join(materials[:3]).lower()} as complementary materials."
    if functions:
        why += f" The plan also accounts for: {', '.join(functions).lower()}."

    return {
        "style": style_name,
        "description": style["description"],
        "room_type": room,
        "palette": palette,
        "walls": style["walls"],
        "flooring": style["flooring"],
        "curtains": style["curtains"],
        "lighting": lighting,
        "decor": decor,
        "furniture": furniture_line + " " + furniture,
        "layout": style["layout"] + " " + layout,
        "space_tip": space_tip,
        "budget_note": budget_note,
        "cost_split": cost_split,
        "budget_df": budget_df,
        "why": why,
        "checklist": key_items,
        "materials": materials,
        "functions": functions,
        "image_query": style["image_query"],
    }

def make_report(prefs, design):
    symbol = CURRENCY_SYMBOL[prefs["currency"]]
    lines = [
        "ROOMMUSE — PERSONAL INTERIOR DESIGN PLAN",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "YOUR PREFERENCES",
        f"Room: {prefs['room_type']}",
        f"Aesthetic: {prefs['style']}",
        f"Room size: {prefs['room_size']}",
        f"Budget level: {prefs['budget_level']}",
        f"Custom budget: {symbol}{prefs['custom_budget']:,.2f}" if prefs["custom_budget"] else "Custom budget: Not specified",
        f"Colours: {', '.join(prefs['colours']) or 'No preference'}",
        f"Furniture: {', '.join(prefs['furniture']) or 'No preference'}",
        f"Lighting: {', '.join(prefs['lighting']) or 'No preference'}",
        f"Materials: {', '.join(prefs['materials']) or 'No preference'}",
        f"Needs: {', '.join(prefs['functions']) or 'No preference'}",
        "",
        "RECOMMENDATIONS",
        f"Overview: {design['description']}",
        f"Wall colours: {design['walls']}",
        f"Flooring: {design['flooring']}",
        f"Curtains: {design['curtains']}",
        f"Furniture: {design['furniture']}",
        f"Lighting: {design['lighting']}",
        f"Decor: {design['decor']}",
        f"Layout: {design['layout']}",
        f"Space-saving tip: {design['space_tip']}",
        f"Why it fits: {design['why']}",
        "",
        "SHOPPING / SETUP CHECKLIST",
    ]
    lines.extend([f"[ ] {item}" for item in design["checklist"]])
    lines += ["", "BUDGET GUIDANCE", design["budget_note"], ""]
    for category, percentage in design["cost_split"].items():
        if prefs["custom_budget"]:
            lines.append(f"{category}: {percentage}% — {symbol}{prefs['custom_budget'] * percentage / 100:,.2f}")
        else:
            lines.append(f"{category}: {percentage}% of the chosen budget")
    lines += [
        "",
        "DISCLAIMER",
        "This is a rule-based design suggestion, not professional architectural advice. Cost allocations are planning estimates only; actual prices depend on room measurements, location, supplier, product quality, installation, and availability. Verify measurements, electrical requirements, ventilation, and safety needs with qualified professionals where appropriate.",
    ]
    return "\n".join(lines)

# ---------------------------------- Interface ----------------------------------
st.markdown("""
<style>
:root { color-scheme: light; }
.block-container { padding-top: 1.8rem; padding-bottom: 3rem; max-width: 1250px; }
.hero { padding: 2rem 2.2rem; border-radius: 22px; background: linear-gradient(120deg, #e9eee5, #f7eee4); margin-bottom: 1.2rem; }
.hero h1 { font-size: clamp(2rem, 4vw, 3.2rem); margin-bottom: .35rem; color: #27372d; }
.hero p { font-size: 1.08rem; color: #45564b; max-width: 760px; }
.small-note { color: #6c746e; font-size: .9rem; }
.swatch { height: 72px; border-radius: 12px; border: 1px solid rgba(0,0,0,.08); }
</style>
""", unsafe_allow_html=True)

if "saved_designs" not in st.session_state:
    st.session_state.saved_designs = []
if "design" not in st.session_state:
    st.session_state.design = None
if "prefs" not in st.session_state:
    st.session_state.prefs = None

st.markdown("""
<div class="hero">
  <h1>RoomMuse 🪴</h1>
  <p>Your personal interior design companion. Choose the mood, colours, needs, and budget — then get a room plan that reflects your taste.</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("Design studio")
    page = st.radio("Navigate", ["Create a design", "Saved designs", "About"])
    st.divider()
    st.caption("RoomMuse uses a built-in rule-based catalogue. No API key is required.")

if page == "Create a design":
    st.subheader("Tell us about your room")
    st.write("You can leave optional preferences empty. Change any selection and generate a new plan whenever you like.")

    with st.form("design_form"):
        left, right = st.columns(2)
        with left:
            room_type = st.selectbox("Room type", ROOMS)
            style = st.selectbox("Preferred aesthetic", list(STYLES.keys()))
            room_size = st.radio("Room size", ["Small", "Medium", "Large"], horizontal=True)
            colours = st.multiselect("Colour preferences", COLOURS, default=["Neutrals"])
            budget_level = st.select_slider("Budget level", options=BUDGET_LEVELS, value="Medium")
            currency = st.selectbox("Currency for your estimate", CURRENCY_OPTIONS, index=0)
            custom_budget = st.number_input(
                "Optional total budget (enter 0 to skip)",
                min_value=0.0, value=0.0, step=5000.0 if currency.startswith("NGN") else 50.0,
                help="This only divides your own budget into suggested categories; it does not fetch live prices.",
            )
        with right:
            furniture = st.multiselect("Furniture preferences", FURNITURE, default=["Modern"])
            lighting = st.multiselect("Lighting preferences", LIGHTING, default=["Warm lighting", "Layered lighting"])
            materials = st.multiselect("Materials and textures", MATERIALS, default=["Wood", "Linen"])
            functions = st.multiselect("What should the room support?", FUNCTIONS, default=["Relaxation", "Storage"])
            extra_notes = st.text_area(
                "Optional notes",
                placeholder="For example: rented apartment, shared room, lots of books, pets, avoid drilling…",
                max_chars=500,
            )
        submitted = st.form_submit_button("✨ Generate My Room Design", type="primary", use_container_width=True)

    if submitted:
        prefs = {
            "room_type": room_type,
            "style": style,
            "room_size": room_size,
            "colours": colours,
            "budget_level": budget_level,
            "currency": currency,
            "custom_budget": float(custom_budget),
            "furniture": furniture,
            "lighting": lighting,
            "materials": materials,
            "functions": functions,
            "extra_notes": extra_notes.strip(),
        }
        st.session_state.prefs = prefs
        st.session_state.design = recommend_design(prefs)

    if st.session_state.design and st.session_state.prefs:
        design = st.session_state.design
        prefs = st.session_state.prefs
        symbol = CURRENCY_SYMBOL[prefs["currency"]]
        st.divider()
        st.subheader(f"Your {design['style']} {design['room_type'].lower()} concept")
        st.write(design["description"])
        a, b, c = st.columns(3)
        a.metric("Aesthetic", design["style"])
        b.metric("Room size", prefs["room_size"])
        c.metric("Budget level", prefs["budget_level"])

        st.markdown("#### Your colour palette")
        swatch_cols = st.columns(len(design["palette"]))
        for col, colour in zip(swatch_cols, design["palette"]):
            with col:
                st.markdown(f'<div class="swatch" style="background:{colour}"></div>', unsafe_allow_html=True)
                st.caption(colour)

        overview_col, detail_col = st.columns([1, 1])
        with overview_col:
            st.markdown("#### Surfaces and styling")
            st.markdown(f"**Wall colours:** {design['walls']}")
            st.markdown(f"**Flooring:** {design['flooring']}")
            st.markdown(f"**Curtains:** {design['curtains']}")
            st.markdown(f"**Decor and accessories:** {design['decor']}")
            st.markdown(f"**Materials you selected:** {', '.join(design['materials']) or 'Flexible — choose what suits your room'}")
        with detail_col:
            st.markdown("#### Furniture and lighting")
            st.write(design["furniture"])
            st.write(design["lighting"])

        st.markdown("#### Suggested furniture arrangement")
        st.write(design["layout"])
        st.info(design["space_tip"])
        st.markdown("#### Why this matches your preferences")
        st.write(design["why"])
        if prefs["extra_notes"]:
            st.markdown("#### Your additional notes")
            st.write(prefs["extra_notes"])
            st.caption("Your notes are included in this session but do not automatically change the rule-based catalogue recommendations.")

        st.markdown("#### Shopping and setup checklist")
        checked_items = []
        check_cols = st.columns(2)
        for idx, item in enumerate(design["checklist"]):
            with check_cols[idx % 2]:
                if st.checkbox(item, key=f"check_{idx}_{design['style']}_{design['room_type']}"):
                    checked_items.append(item)

        st.markdown("#### Suggested budget breakdown")
        st.caption("Percentages are planning allocations, not live market prices or supplier quotes.")
        budget_df = design["budget_df"].copy()
        if prefs["custom_budget"]:
            budget_df["Estimated amount"] = budget_df["Estimated amount"].map(lambda x: f"{symbol}{x:,.2f}")
            st.dataframe(budget_df, hide_index=True, use_container_width=True)
            st.metric("Total budget entered", f"{symbol}{prefs['custom_budget']:,.2f}")
        else:
            st.dataframe(budget_df[["Category", "Allocation (%)"]], hide_index=True, use_container_width=True)
            st.caption("Enter a custom budget above and regenerate to see indicative allocations in your selected currency.")
        st.write(design["budget_note"])

        with st.expander("Design inspiration images"):
            st.write("These links open image-search results for visual inspiration. They are not generated images, and external results may vary.")
            from urllib.parse import quote_plus
            image_url = "https://www.google.com/search?tbm=isch&q=" + quote_plus(f"{design['image_query']} {design['room_type']}")
            st.markdown(f"[Open inspiration image search ↗]({image_url})")
            st.caption("Use images as references, and check usage rights before reusing them in a public project.")

        with st.expander("Compare with another aesthetic"):
            comparison_style = st.selectbox(
                "Choose a second style",
                [s for s in STYLES if s != design["style"]],
                key="comparison_style",
            )
            compare = STYLES[comparison_style]
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"**Current: {design['style']}**")
                st.write(design["description"])
                st.write(f"Palette: {', '.join(design['palette'])}")
                st.write(f"Furniture: {STYLES[design['style']]['furniture']}")
            with c2:
                st.markdown(f"**Alternative: {comparison_style}**")
                st.write(compare["description"])
                st.write(f"Palette: {', '.join(compare['palette'])}")
                st.write(f"Furniture: {compare['furniture']}")
            st.caption("Compare the atmosphere and materials before choosing. This is a qualitative comparison, not a product or price comparison.")

        report = make_report(prefs, design)
        st.download_button(
            "⬇️ Download design report (.txt)",
            data=report.encode("utf-8"),
            file_name="roommuse_design_plan.txt",
            mime="text/plain",
            use_container_width=True,
        )
        if st.button("♡ Save this design to favourites", use_container_width=True):
            st.session_state.saved_designs.append({
                "saved_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "style": design["style"],
                "room_type": design["room_type"],
                "report": report,
            })
            st.success("Design saved for this browser session.")
        st.caption("Favourites are kept in Streamlit's session state and may disappear when the session resets.")
        st.warning("Budget disclaimer: amounts are only category allocations based on the budget you enter. They are not verified local prices. Check dimensions, product suitability, electrical requirements, ventilation, and safety with qualified professionals where appropriate.")

elif page == "Saved designs":
    st.subheader("Your saved designs")
    if not st.session_state.saved_designs:
        st.info("You have not saved any designs in this session yet. Create a design and select “Save this design to favourites”.")
    else:
        for i, item in enumerate(reversed(st.session_state.saved_designs)):
            with st.expander(f"{item['room_type']} — {item['style']} ({item['saved_at']})", expanded=(i == 0)):
                st.download_button(
                    "Download this plan",
                    data=item["report"].encode("utf-8"),
                    file_name=f"roommuse_{item['room_type'].lower().replace(' ', '_')}_{item['style'].lower().replace(' ', '_')}.txt",
                    mime="text/plain",
                    key=f"download_saved_{i}",
                )
                st.text(item["report"])
        if st.button("Clear saved designs"):
            st.session_state.saved_designs = []
            st.success("Saved designs cleared for this session.")

else:
    st.subheader("About RoomMuse")
    st.write(
        "RoomMuse is a beginner-friendly interior design recommendation demo built with Streamlit. "
        "It maps user-selected room types, aesthetics, colours, needs, and budgets to a curated catalogue of suggestions."
    )
    st.markdown("""
    **What it does**
    - Generates a style-led room concept and coordinated colour palette.
    - Suggests furniture, lighting, surfaces, layout, and a setup checklist.
    - Allocates an optional user-entered budget by category.
    - Offers image-search inspiration and a downloadable text report.

    **Current limitations**
    - Recommendations use rules and a built-in catalogue, not a trained machine-learning model.
    - It does not inspect room photos, measure a room, generate images, or retrieve live product prices.
    - Saved favourites are session-only; there is no database or user login.
    - The image inspiration feature opens a search page rather than embedding or licensing images.

    **Possible future upgrades**
    - Room photo upload and visual analysis.
    - AI API integration using environment variables or Streamlit secrets.
    - Locally relevant supplier catalogue and verified pricing.
    - Persistent user accounts and saved projects.
    - PDF export and interactive floor-plan tools.
    """)
    st.caption("Built for learning and portfolio demonstration. Always verify measurements, materials, accessibility, ventilation, and safety before purchasing or installing anything.")
