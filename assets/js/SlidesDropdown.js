document.addEventListener('DOMContentLoaded', () => {
    const dropdowns = Array.prototype.slice.call(document.querySelectorAll('[data-slides-dropdown]'), 0);
    const burgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0);

    const closeDropdown = (dropdown, options = {}) => {
        const button = dropdown.querySelector('[data-slides-dropdown-button]');
        dropdown.classList.remove('is-open', 'is-aligned-right');
        if (button) {
            button.setAttribute('aria-expanded', 'false');
            if (options.returnFocus) {
                button.focus();
            }
        }
    };

    const closeAllDropdowns = () => {
        dropdowns.forEach((dropdown) => closeDropdown(dropdown));
    };

    dropdowns.forEach((dropdown) => {
        const button = dropdown.querySelector('[data-slides-dropdown-button]');
        const panel = dropdown.querySelector('[data-slides-dropdown-panel]');
        if (!button || !panel) return;

        let openedByFocus = false;
        let autoOpenSuppressed = false;

        const clampPanelToViewport = () => {
            dropdown.classList.remove('is-aligned-right');
            window.requestAnimationFrame(() => {
                const panelRect = panel.getBoundingClientRect();
                if (panelRect.right > window.innerWidth - 16) {
                    dropdown.classList.add('is-aligned-right');
                }
            });
        };

        const setOpen = (isOpen, options = {}) => {
            if (isOpen && autoOpenSuppressed && options.source !== 'click') return;

            dropdown.classList.toggle('is-open', isOpen);
            button.setAttribute('aria-expanded', String(isOpen));

            if (isOpen) {
                openedByFocus = options.source === 'focus';
                clampPanelToViewport();
            } else {
                openedByFocus = false;
                dropdown.classList.remove('is-aligned-right');
            }
        };

        dropdown.addEventListener('pointerenter', (event) => {
            if (event.pointerType === 'touch') return;
            setOpen(true, { source: 'hover' });
        });

        dropdown.addEventListener('pointerleave', (event) => {
            if (event.pointerType === 'touch') return;
            autoOpenSuppressed = false;
            setOpen(false);
        });

        dropdown.addEventListener('focusin', () => {
            setOpen(true, { source: 'focus' });
        });

        dropdown.addEventListener('focusout', () => {
            window.setTimeout(() => {
                if (!dropdown.contains(document.activeElement)) {
                    autoOpenSuppressed = false;
                    setOpen(false);
                }
            }, 0);
        });

        const closeFromEscape = (event) => {
            if (!dropdown.classList.contains('is-open')) return;

            event.preventDefault();
            autoOpenSuppressed = true;
            setOpen(false);
            button.focus();
        };

        dropdown.addEventListener('keydown', (event) => {
            if (event.key === 'Escape') {
                closeFromEscape(event);
            }
        });

        document.addEventListener('keydown', (event) => {
            if (event.key === 'Escape') {
                closeFromEscape(event);
            }
        });

        button.addEventListener('click', (event) => {
            event.preventDefault();
            autoOpenSuppressed = false;

            if (dropdown.classList.contains('is-open') && openedByFocus) {
                openedByFocus = false;
                setOpen(true, { source: 'click' });
                return;
            }

            setOpen(!dropdown.classList.contains('is-open'), { source: 'click' });
        });

        panel.addEventListener('click', (event) => {
            if (event.target.closest('a')) {
                autoOpenSuppressed = false;
                setOpen(false);
            }
        });
    });

    document.addEventListener('pointerdown', (event) => {
        dropdowns.forEach((dropdown) => {
            if (!dropdown.contains(event.target)) {
                closeDropdown(dropdown);
            }
        });
    });

    burgers.forEach((burger) => {
        burger.addEventListener('click', () => {
            const targetId = burger.dataset.target;
            const target = targetId ? document.getElementById(targetId) : null;
            const isExpanded = Boolean(target && target.classList.contains('is-active'));

            burger.setAttribute('aria-expanded', String(isExpanded));

            if (!isExpanded) {
                closeAllDropdowns();
            }
        });
    });
});
