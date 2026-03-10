# ui/sidebar.py
import streamlit as st
import json

def render_sidebar():
    """Génère la barre latérale et retourne le dictionnaire de configuration centralisée."""
    
    LANGUAGES_DICT = {
        "fr": "Français", "en": "Anglais", "es": "Espagnol",
        "de": "Allemand", "it": "Italien", "ar": "Arabe", "zh": "Chinois"
    }

    with st.sidebar:
        st.markdown("<h3 style='margin-top: -40px; margin-bottom: 20px; font-size: 1.1em;'>Configuration du Run</h3>", unsafe_allow_html=True)
        


        def get_default(key, default_val):
            return st.session_state.get(f"config_{key}", default_val)
        
        # 1. Sélection du Modèle / Provider
        with st.expander("Modèle", expanded=True):
            prov_def = get_default("provider", "Google Gemini (API)")
            provider = st.selectbox("Provider", ["Google Gemini (API)", "Ollama (Local)"], index=0 if prov_def=="Google Gemini (API)" else 1)
            
            if provider == "Google Gemini (API)":
                mod_def = get_default("model", "gemini-2.5-flash")
                options_models = ["gemini-2.5-flash"]
                mod_idx = options_models.index(mod_def) if mod_def in options_models else 0
                model_name = st.selectbox("Modèle", options_models, index=mod_idx)
                st.caption("via Google AI Studio (Free Tier)")
            else:
                mod_def = get_default("model", "mistral-nemo")
                options_models = ["mistral-nemo", "llama3"]
                mod_idx = options_models.index(mod_def) if mod_def in options_models else 0
                model_name = st.selectbox("Modèle", options_models, index=mod_idx)
                st.caption("Modèle On-premise (12B)")
            
        # 2. Données et Langues
        with st.expander("Données et Langues", expanded=True):
            ds_def = get_default("dataset_type", "unspecific")
            dataset_type = st.radio("Dataset", ["unspecific (Diversité)", "specific (Robustesse)"], index=0 if "unspecific" in ds_def else 1)
            
            if st.button("Toutes les langues"):
                st.session_state["config_languages"] = list(LANGUAGES_DICT.keys())
                
            selected_langs = st.multiselect(
                "Langues", 
                options=list(LANGUAGES_DICT.keys()),
                format_func=lambda x: LANGUAGES_DICT[x],
                default=get_default("languages", ["fr", "en", "es", "de", "it"])
            )
            
            if len(selected_langs) < 5:
                st.warning("La baseline exige au moins 5 langues.")
        
        # 3. Variantes 
        with st.expander("Stratégie (Variantes)", expanded=True):
            var_def = get_default("variant", "Baseline (Vanilla)")
            var_options = ["Baseline (Vanilla)", "System Prompt", "Reformulation auto"]
            var_idx = var_options.index(var_def) if var_def in var_options else 0
            variant = st.selectbox("Expérience", var_options, index=var_idx)
        
        # 4. Hyperparamètres (Centralisés)
        with st.expander("Paramètres", expanded=False):
            temperature = st.slider("Température", 0.0, 2.0, get_default("temperature", 0.0), 0.1)
            top_p = st.slider("Top-p", 0.0, 1.0, get_default("top_p", 1.0), 0.05)
            max_tokens = st.number_input("Max Tokens", 10, 2048, get_default("max_tokens", 500), step=50)
            seed_val = get_default("seed", 42)
            seed = st.number_input("Déterminisme (Seed)", 0, 100000, seed_val if seed_val is not None else 42)

        # Retourne la configuration complète pour assurer la reproductibilité
        # (Cette configuration sera sauvegardée dans le metadata.json final)
        config_dict = {
            "provider": provider,
            "model": model_name,
            "dataset_type": dataset_type.split(" ")[0],
            "languages": selected_langs,
            "variant": variant,
            "temperature": temperature,
            "top_p": top_p,
            "max_tokens": max_tokens,
            "seed": seed
        }
        
        for k, v in config_dict.items():
            st.session_state[f"config_{k}"] = v
            
        return config_dict