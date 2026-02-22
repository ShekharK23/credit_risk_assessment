/**
 * 1. Dropdown: toggle menu, close on outside click.
 * 2. Tabs: on index page, tab-link clicks show section and sync hash; close dropdown when item selected.
 */
(function () {
	function run() {
		var menuBtn = document.getElementById('nav-menu-btn');
		var dropdown = document.getElementById('nav-dropdown');
		var wrap = document.getElementById('nav-dropdown-wrap');
		var chevron = document.querySelector('.nav-menu-chevron');
		var panels = document.querySelectorAll('.tab-panel');
		var tabLinks = document.querySelectorAll('.tab-link');
		var onIndex = (window.location.pathname === '/' || window.location.pathname === '');

		function closeDropdown() {
			if (dropdown) {
				dropdown.classList.remove('is-open');
				dropdown.setAttribute('aria-hidden', 'true');
			}
			if (menuBtn) {
				menuBtn.setAttribute('aria-expanded', 'false');
			}
			if (chevron) chevron.classList.remove('is-open');
		}

		function openDropdown() {
			if (dropdown) {
				dropdown.classList.add('is-open');
				dropdown.setAttribute('aria-hidden', 'false');
			}
			if (menuBtn) menuBtn.setAttribute('aria-expanded', 'true');
			if (chevron) chevron.classList.add('is-open');
		}

		function toggleDropdown() {
			var isOpen = dropdown && dropdown.classList.contains('is-open');
			if (isOpen) closeDropdown();
			else openDropdown();
		}

		if (menuBtn && dropdown) {
			menuBtn.addEventListener('click', function (e) {
				e.stopPropagation();
				toggleDropdown();
			});

			document.addEventListener('click', function (e) {
				if (wrap && !wrap.contains(e.target)) closeDropdown();
			});

			document.addEventListener('keydown', function (e) {
				if (e.key === 'Escape') closeDropdown();
			});
		}

		function showSection(sectionId) {
			panels.forEach(function (p) {
				var isTarget = p.id === 'section-' + sectionId;
				p.classList.toggle('hidden', !isTarget);
			});
			if (history.replaceState) history.replaceState(null, '', '#' + sectionId);
			closeDropdown();
		}

		function getSectionFromHash() {
			var hash = (window.location.hash || '#home').slice(1);
			return hash && document.getElementById('section-' + hash) ? hash : 'home';
		}

		tabLinks.forEach(function (link) {
			link.addEventListener('click', function (e) {
				var sectionId = link.getAttribute('data-section');
				if (!sectionId) return;
				if (onIndex) {
					e.preventDefault();
					showSection(sectionId);
				}
			});
		});

		document.querySelectorAll('.go-to-tab').forEach(function (btn) {
			btn.addEventListener('click', function () {
				var sectionId = this.getAttribute('data-section');
				if (sectionId) showSection(sectionId);
			});
		});

		window.addEventListener('hashchange', function () {
			if (panels.length) showSection(getSectionFromHash());
		});

		if (panels.length) showSection(getSectionFromHash());
	}

	if (document.readyState === 'loading') {
		document.addEventListener('DOMContentLoaded', run);
	} else {
		run();
	}
})();
