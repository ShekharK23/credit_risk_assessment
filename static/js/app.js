/**
 * Tab navigation: show/hide sections and sync URL hash.
 * Runs only when .tab-panel and #main-nav exist (index page).
 */
(function () {
	function initTabs() {
		var panels = document.querySelectorAll('.tab-panel');
		var tabs = document.querySelectorAll('.tab-link');
		var nav = document.getElementById('main-nav');

		if (!nav || !panels.length) return;

		function showSection(sectionId) {
			panels.forEach(function (p) {
				var isTarget = p.id === 'section-' + sectionId;
				p.classList.toggle('hidden', !isTarget);
			});
			tabs.forEach(function (t) {
				var isActive = t.getAttribute('data-section') === sectionId;
				t.classList.toggle('bg-accent/20', isActive);
				t.setAttribute('aria-selected', isActive ? 'true' : 'false');
			});
			if (history.replaceState) history.replaceState(null, '', '#' + sectionId);
		}

		function getSectionFromHash() {
			var hash = (window.location.hash || '#home').slice(1);
			return hash && document.getElementById('section-' + hash) ? hash : 'home';
		}

		nav.addEventListener('click', function (e) {
			var t = e.target.closest('.tab-link');
			if (!t) return;
			var sectionId = t.getAttribute('data-section');
			var onIndex = window.location.pathname === '/' || window.location.pathname === '';
			if (sectionId && onIndex) {
				e.preventDefault();
				showSection(sectionId);
			}
		});

		document.querySelectorAll('.go-to-tab').forEach(function (btn) {
			btn.addEventListener('click', function () {
				var sectionId = this.getAttribute('data-section');
				if (sectionId) showSection(sectionId);
			});
		});

		window.addEventListener('hashchange', function () {
			showSection(getSectionFromHash());
		});

		showSection(getSectionFromHash());
	}

	if (document.readyState === 'loading') {
		document.addEventListener('DOMContentLoaded', initTabs);
	} else {
		initTabs();
	}
})();
