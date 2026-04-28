const playerId = window.location.pathname.split('/').pop();

function fmt(val, decimals = 1) {
    return val !== undefined && val !== null ? Number(val).toFixed(decimals) : '—';
}

function pct(val) {
    return val !== undefined && val !== null ? (Number(val) * 100).toFixed(1) + '%' : '—';
}

async function loadPlayer() {
    try {
        const infoRes = await fetch(`/api/player/${playerId}/info`);
        const info = await infoRes.json();

        document.getElementById('player-name').textContent = info.name || '—';
        document.getElementById('player-meta').textContent =
            [info.team, info.position].filter(Boolean).join(' · ') || '—';
        document.getElementById('player-jersey').textContent =
            info.jersey ? `#${info.jersey}` : '';
        document.getElementById('bio-height').textContent = info.height || '—';
        document.getElementById('bio-weight').textContent = info.weight ? `${info.weight} lbs` : '—';
        document.getElementById('bio-country').textContent = info.country || '—';
        document.getElementById('bio-experience').textContent =
            info.experience !== undefined ? `${info.experience} yr${info.experience !== 1 ? 's' : ''}` : '—';

        document.title = `${info.name} — the NBA house`;

        document.getElementById('player-headshot').src =
            `https://cdn.nba.com/headshots/nba/latest/1040x760/${playerId}.png`;

    } catch (e) {
        document.getElementById('player-name').textContent = 'Error loading player';
    }
}

async function loadCareer() {
    try {
        const res = await fetch(`/api/player/${playerId}/career`);
        const career = await res.json();

        document.getElementById('career-loading').style.display = 'none';

        if (!Array.isArray(career) || !career.length) return;

        const tbody = document.getElementById('career-rows');
        tbody.innerHTML = career.map(row => `
            <tr>
                <td>${row.SEASON_ID || '—'}</td>
                <td>${row.TEAM_ABBREVIATION || '—'}</td>
                <td>${row.GP || '—'}</td>
                <td>${fmt(row.MIN)}</td>
                <td>${fmt(row.PTS)}</td>
                <td>${fmt(row.REB)}</td>
                <td>${fmt(row.AST)}</td>
                <td>${fmt(row.STL)}</td>
                <td>${fmt(row.BLK)}</td>
                <td>${pct(row.FG_PCT)}</td>
                <td>${pct(row.FG3_PCT)}</td>
                <td>${pct(row.FT_PCT)}</td>
                <td>${fmt(row.TOV)}</td>
            </tr>
        `).join('');

        document.getElementById('career-section').style.display = 'block';
    } catch (e) {
        document.getElementById('career-loading').style.display = 'none';
    }
}

async function loadGameLog() {
    try {
        const res = await fetch(`/api/player/${playerId}/gamelog?season=2024-25`);
        const log = await res.json();

        if (!Array.isArray(log) || !log.length) return;

        const tbody = document.getElementById('gamelog-rows');
        tbody.innerHTML = log.map(row => `
            <tr class="${row.WL === 'W' ? 'row-win' : 'row-loss'}">
                <td>${row.GAME_DATE || '—'}</td>
                <td>${row.MATCHUP || '—'}</td>
                <td class="wl-cell ${row.WL === 'W' ? 'win' : 'loss'}">${row.WL || '—'}</td>
                <td>${row.MIN || '—'}</td>
                <td>${fmt(row.PTS)}</td>
                <td>${fmt(row.REB)}</td>
                <td>${fmt(row.AST)}</td>
                <td>${fmt(row.STL)}</td>
                <td>${fmt(row.BLK)}</td>
                <td>${pct(row.FG_PCT)}</td>
                <td class="${row.PLUS_MINUS > 0 ? 'plus' : row.PLUS_MINUS < 0 ? 'minus' : ''}">${row.PLUS_MINUS > 0 ? '+' : ''}${row.PLUS_MINUS ?? '—'}</td>
            </tr>
        `).join('');

        document.getElementById('gamelog-section').style.display = 'block';
    } catch (e) {}
}

loadPlayer();
loadCareer();
loadGameLog();
