function toggleDetails(hanja, original_word, text_language_no_related, text_language_error) {
    const detailsDiv = document.getElementById(`details-${hanja}`);
    const resultItem = detailsDiv.closest('.result-item'); // Get the parent .result-item
    if (detailsDiv) {
        // Toggle the 'visible' class on the details div
        detailsDiv.classList.toggle('visible');

        // Update the parent .result-item's 'collapsed' class
        if (detailsDiv.classList.contains('visible')) {
            resultItem.classList.remove('collapsed'); // Expanded state
        } else {
            resultItem.classList.add('collapsed'); // Collapsed state
        }

        // If it's visible and data isn't loaded, fetch related words
        if (detailsDiv.classList.contains('visible') && !detailsDiv.dataset.loaded) {
            fetchRelatedWords(hanja, detailsDiv, original_word, text_language_no_related, text_language_error);
        }
    }
}


async function fetchRelatedWords(hanja, container, originalWord, text_language_no_related, text_language_error) {
    try {
        // Fetch data from your server
        const response = await fetch(`/related-words?hanja=${encodeURIComponent(hanja)}&original_word=${encodeURIComponent(originalWord)}`);
        const data = await response.json();
        // Escape special characters to prevent XSS
        const sanitizeHTML = (str) =>
            String(str)
                .replace(/&/g, "&amp;")
                .replace(/</g, "&lt;")
                .replace(/>/g, "&gt;")
                .replace(/"/g, "&quot;")
                .replace(/'/g, "&#39;");

        // Check if data is not empty
        if (data.length > 0) {
            // Populate the container with the related words based on language
            container.innerHTML = data
                .map((word) => {
                    const sanitizedWord = sanitizeHTML(word.word);
                    const sanitizedHanja = sanitizeHTML(word.hanja);
                    const sanitizedLemma = sanitizeHTML(word.lemma);

                    return `
                        <form action="/search" method="POST" class="related-word-form">
                            <input type="hidden" name="word" value="${sanitizedWord}">
                            <button type="submit" class="related-word-button">
                                <strong>${sanitizedWord}</strong></button> (${sanitizedHanja}) : ${sanitizedLemma}
                        </form>
                    `;
                })
                .join('');
        } else {
            // Display a message if no related words are found
            container.innerHTML = `${text_language_no_related}`;
        }

        // Mark as loaded to avoid re-fetching
        container.dataset.loaded = true;
    } catch (error) {
        console.error('Error fetching related words:', error);
        container.innerHTML = `${text_language_error}`;
    }
}

const playButton = document.getElementById("play-button");

// Check if the playButton exists before adding the event listener
if (playButton) {
    const audio = document.getElementById("audio-player");
playButton.addEventListener("click", () => {
    if (audio.paused) {
        audio.play();
        playButton.textContent = "⏸"; // Change le bouton en pause
    } else {
        audio.pause();
        playButton.textContent = "▶"; // Remet l'icône play
    }
});
}

document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.querySelector('input[data-autocomplete="word"]');
    const suggestionList = document.querySelector(".autocomplete-list");

    if (!searchInput || !suggestionList) {
        return;
    }

    let activeIndex = -1;
    let debounceTimer = null;
    let currentController = null;

    const clearSuggestions = () => {
        suggestionList.innerHTML = "";
        suggestionList.style.display = "none";
        activeIndex = -1;
    };

    const setActiveItem = (index) => {
        const items = suggestionList.querySelectorAll("li");
        items.forEach((item, idx) => {
            item.classList.toggle("active", idx === index);
        });
    };

    const applySuggestion = (value) => {
        searchInput.value = value;
        clearSuggestions();
    };

    const fetchSuggestions = async (query) => {
        if (currentController) {
            currentController.abort();
        }
        currentController = new AbortController();

        try {
            const response = await fetch(`/autocomplete?q=${encodeURIComponent(query)}`, {
                signal: currentController.signal,
            });
            if (!response.ok) {
                clearSuggestions();
                return;
            }
            const suggestions = await response.json();
            if (!Array.isArray(suggestions) || suggestions.length === 0) {
                clearSuggestions();
                return;
            }
            suggestionList.innerHTML = "";
            suggestions.forEach((suggestion) => {
                const item = document.createElement("li");
                item.textContent = suggestion;
                item.addEventListener("mousedown", (event) => {
                    event.preventDefault();
                    applySuggestion(suggestion);
                    searchInput.closest("form").submit();
                });
                suggestionList.appendChild(item);
            });
            suggestionList.style.display = "block";
        } catch (error) {
            if (error.name !== "AbortError") {
                clearSuggestions();
            }
        }
    };

    searchInput.addEventListener("input", (event) => {
        const query = event.target.value.trim().replace(/\s+/g, "");
        if (debounceTimer) {
            clearTimeout(debounceTimer);
        }
        if (!query) {
            clearSuggestions();
            return;
        }
        debounceTimer = setTimeout(() => {
            fetchSuggestions(query);
        }, 200);
    });

    searchInput.addEventListener("keydown", (event) => {
        const items = suggestionList.querySelectorAll("li");
        if (items.length === 0) {
            return;
        }
        if (event.key === "ArrowDown") {
            event.preventDefault();
            activeIndex = (activeIndex + 1) % items.length;
            setActiveItem(activeIndex);
        } else if (event.key === "ArrowUp") {
            event.preventDefault();
            activeIndex = (activeIndex - 1 + items.length) % items.length;
            setActiveItem(activeIndex);
        } else if (event.key === "Enter" && activeIndex >= 0) {
            event.preventDefault();
            applySuggestion(items[activeIndex].textContent);
            searchInput.closest("form").submit();
        } else if (event.key === "Escape") {
            clearSuggestions();
        }
    });

    searchInput.addEventListener("blur", () => {
        setTimeout(() => {
            clearSuggestions();
        }, 150);
    });
});

// ---------- Theme picker (colour palette + background), saved in localStorage ----------
const THEMES = ["rose", "jade", "indigo", "persimmon", "lavender", "seal", "night"];
const BACKGROUNDS = ["plain", "gradient", "hanji", "lattice", "waves"];

function readSetting(key, allowed, fallback) {
    try {
        const value = localStorage.getItem(key);
        return allowed.includes(value) ? value : fallback;
    } catch (e) {
        return fallback;
    }
}

function saveSetting(key, value) {
    try {
        localStorage.setItem(key, value);
    } catch (e) {
        // Storage can be unavailable (private mode, blocked cookies): the choice then lasts for this page only
    }
}

function applyAppearance(theme, background) {
    const root = document.documentElement;
    if (theme === "rose") {
        root.removeAttribute("data-theme");
    } else {
        root.setAttribute("data-theme", theme);
    }
    if (background === "plain") {
        root.removeAttribute("data-bg");
    } else {
        root.setAttribute("data-bg", background);
    }
    document.querySelectorAll("[data-theme-value]").forEach((button) => {
        button.setAttribute("aria-pressed", String(button.dataset.themeValue === theme));
    });
    document.querySelectorAll("[data-bg-value]").forEach((button) => {
        button.setAttribute("aria-pressed", String(button.dataset.bgValue === background));
    });
}

document.addEventListener("DOMContentLoaded", () => {
    const toggle = document.querySelector(".theme-toggle");
    const panel = document.getElementById("theme-panel");
    if (!toggle || !panel) {
        return;
    }

    let theme = readSetting("hg-theme", THEMES, "rose");
    let background = readSetting("hg-bg", BACKGROUNDS, "plain");
    applyAppearance(theme, background);

    const setOpen = (open) => {
        panel.hidden = !open;
        toggle.setAttribute("aria-expanded", String(open));
    };

    toggle.addEventListener("click", (event) => {
        event.stopPropagation();
        setOpen(panel.hidden);
    });

    panel.addEventListener("click", (event) => {
        event.stopPropagation();
        const themeButton = event.target.closest("[data-theme-value]");
        const bgButton = event.target.closest("[data-bg-value]");
        if (themeButton) {
            theme = themeButton.dataset.themeValue;
            saveSetting("hg-theme", theme);
        } else if (bgButton) {
            background = bgButton.dataset.bgValue;
            saveSetting("hg-bg", background);
        } else {
            return;
        }
        applyAppearance(theme, background);
    });

    document.addEventListener("click", () => setOpen(false));
    document.addEventListener("keydown", (event) => {
        if (event.key === "Escape" && !panel.hidden) {
            setOpen(false);
            toggle.focus();
        }
    });
});

// ---------- Personal dictionary: saved words and history, stored in localStorage ----------
const SAVED_KEY = "hg-saved-words";
const HISTORY_KEY = "hg-history";
const HISTORY_LIMIT = 100;

// Some definitions come from the database with HTML entities (&quot;): turn them back into plain text
function decodeEntities(text) {
    return new DOMParser().parseFromString(String(text || ""), "text/html").documentElement.textContent;
}

function readList(key) {
    try {
        const list = JSON.parse(localStorage.getItem(key) || "[]");
        return Array.isArray(list) ? list : [];
    } catch (e) {
        return [];
    }
}

function writeList(key, list) {
    try {
        localStorage.setItem(key, JSON.stringify(list));
    } catch (e) {
        // Storage unavailable (private mode, blocked cookies): nothing is kept
    }
}

const sameEntry = (a, b) => a.word === b.word && (a.hanja || "") === (b.hanja || "");

function entryFromButton(button) {
    return {
        word: button.dataset.word,
        hanja: button.dataset.hanja || "",
        lemma: decodeEntities(button.dataset.lemma),
    };
}

function isSaved(entry) {
    return readList(SAVED_KEY).some((item) => sameEntry(item, entry));
}

function toggleSaved(entry) {
    const saved = readList(SAVED_KEY);
    const index = saved.findIndex((item) => sameEntry(item, entry));
    if (index >= 0) {
        saved.splice(index, 1);
    } else {
        saved.unshift({ ...entry, date: Date.now() });
    }
    writeList(SAVED_KEY, saved);
    return index < 0;
}

function addToHistory(entry) {
    const history = readList(HISTORY_KEY).filter((item) => !sameEntry(item, entry));
    history.unshift({ ...entry, date: Date.now() });
    writeList(HISTORY_KEY, history.slice(0, HISTORY_LIMIT));
}

function updateStar(button, saved) {
    const labels = document.body.dataset;
    const label = saved ? labels.labelUnsave : labels.labelSave;
    button.setAttribute("aria-pressed", String(saved));
    button.setAttribute("aria-label", label);
    button.title = label;
}

// Results page: star buttons, and every word shown is added to the history
document.addEventListener("DOMContentLoaded", () => {
    const buttons = document.querySelectorAll(".save-word");
    // Add in reverse so the first result ends up at the top of the history
    Array.from(buttons).reverse().forEach((button) => addToHistory(entryFromButton(button)));
    buttons.forEach((button) => {
        updateStar(button, isSaved(entryFromButton(button)));
        button.addEventListener("click", () => {
            updateStar(button, toggleSaved(entryFromButton(button)));
        });
    });
});

// Personal dictionary page
document.addEventListener("DOMContentLoaded", () => {
    const page = document.querySelector(".dictionary-page");
    if (!page) {
        return;
    }
    const removeLabel = page.dataset.labelRemove;
    const tabs = page.querySelectorAll("[role=tab]");
    const clearButton = page.querySelector(".clear-history");

    const searchLink = (entry) => {
        const form = document.createElement("form");
        form.method = "POST";
        form.action = "/search";
        form.className = "word-link-form";
        const input = document.createElement("input");
        input.type = "hidden";
        input.name = "word";
        input.value = entry.word;
        const button = document.createElement("button");
        button.type = "submit";
        button.className = "word-link";
        const word = document.createElement("strong");
        word.textContent = entry.word;
        button.appendChild(word);
        if (entry.hanja) {
            const hanja = document.createElement("span");
            hanja.className = "word-hanja";
            hanja.textContent = entry.hanja;
            button.appendChild(hanja);
        }
        form.append(input, button);
        return form;
    };

    const render = (name) => {
        const key = name === "saved" ? SAVED_KEY : HISTORY_KEY;
        const list = readList(key);
        const container = page.querySelector(`[data-list="${name}"]`);
        container.innerHTML = "";
        list.forEach((entry) => {
            const item = document.createElement("li");
            item.className = "word-entry";
            item.appendChild(searchLink(entry));
            if (entry.lemma) {
                const lemma = document.createElement("span");
                lemma.className = "word-lemma";
                lemma.textContent = entry.lemma;
                item.appendChild(lemma);
            }
            if (name === "saved") {
                const remove = document.createElement("button");
                remove.type = "button";
                remove.className = "remove-word";
                remove.textContent = "×";
                remove.title = removeLabel;
                remove.setAttribute("aria-label", `${removeLabel} ${entry.word}`);
                remove.addEventListener("click", () => {
                    writeList(SAVED_KEY, readList(SAVED_KEY).filter((saved) => !sameEntry(saved, entry)));
                    render("saved");
                });
                item.appendChild(remove);
            }
            container.appendChild(item);
        });
        page.querySelector(`[data-empty="${name}"]`).hidden = list.length > 0;
        page.querySelector(`[data-count="${name}"]`).textContent = list.length ? `(${list.length})` : "";
        if (name === "history") {
            clearButton.hidden = list.length === 0;
        }
    };

    const selectTab = (tab) => {
        tabs.forEach((other) => {
            const selected = other === tab;
            other.setAttribute("aria-selected", String(selected));
            other.tabIndex = selected ? 0 : -1;
            document.getElementById(other.getAttribute("aria-controls")).hidden = !selected;
        });
    };

    tabs.forEach((tab, index) => {
        tab.addEventListener("click", () => selectTab(tab));
        tab.addEventListener("keydown", (event) => {
            if (event.key === "ArrowRight" || event.key === "ArrowLeft") {
                const next = tabs[(index + (event.key === "ArrowRight" ? 1 : tabs.length - 1)) % tabs.length];
                selectTab(next);
                next.focus();
            }
        });
    });

    clearButton.addEventListener("click", () => {
        writeList(HISTORY_KEY, []);
        render("history");
    });

    render("saved");
    render("history");
});
