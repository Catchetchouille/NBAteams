const teamId = window.location.pathname.split('/').pop();

async function loadTeam() {
    const [teamRes, rosterRes] = await Promise.all([
        fetch(`/api/team/${teamId}/info`),
        fetch(`/api/team/${teamId}/roster`)
    ]);

    const teamInfo = await teamRes.json();
    const roster = await rosterRes.json();

    document.getElementById('team-name').textContent = teamInfo.name || 'Team';
    document.getElementById('team-logo').src =
        `https://cdn.nba.com/logos/nba/${teamId}/global/L/logo.svg`;
    document.title = `${teamInfo.name} — the NBA house`;

    const tbody = document.getElementById('player-rows');
    if (!roster.length) {
        tbody.innerHTML = '<tr><td colspan="3">No players found.</td></tr>';
        return;
    }

    const rows = roster.map((player) => `
        <tr class="player-row" onclick="window.location.href='/player/${player.id}'" title="Click to view stats">
            <td>
                <img src="https://cdn.nba.com/headshots/nba/latest/1040x760/${player.id}.png"
                     alt="${player.name}"
                     class="roster-headshot"
                     onerror="this.style.display='none'">
                ${player.name}
            </td>
            <td>${player.position || 'N/A'}</td>
            <td>${player.season || 'N/A'}</td>
        </tr>
    `);

    tbody.innerHTML = rows.join('');
}

function searchTable() {
    const input = document.getElementById("searchInput").value.toLowerCase();
    const table = document.getElementById("myTable");
    const rows = table.getElementsByTagName("tr");
    for (let i = 1; i < rows.length; i++) {
        const nameCell = rows[i].getElementsByTagName("td")[0];
        if (nameCell) {
            const name = nameCell.innerText.toLowerCase();
            rows[i].style.display = name.includes(input) ? "" : "none";
        }
    }
}

async function openPlayerModal(playerId, name, position, jersey) {
    document.getElementById('modal-name').textContent = name;
    document.getElementById('modal-team-pos').textContent = position;
    document.getElementById('modal-jersey').textContent = jersey !== 'N/A' ? `#${jersey}` : '';
    document.getElementById('modal-headshot').src =
        `https://cdn.nba.com/headshots/nba/latest/1040x760/${playerId}.png`;
    document.getElementById('modal-headshot').style.display = '';
    document.getElementById('modal-height').textContent = '—';
    document.getElementById('modal-weight').textContent = '—';
    document.getElementById('modal-country').textContent = '—';
    document.getElementById('modal-experience').textContent = '—';
    document.getElementById('modal-loading').style.display = 'block';
    document.getElementById('modal-career').style.display = 'none';

    document.getElementById('player-modal').classList.add('active');
    document.body.style.overflow = 'hidden';

    try {
        const [infoRes, careerRes] = await Promise.all([
            fetch(`/api/player/${playerId}/info`),
            fetch(`/api/player/${playerId}/career`)
        ]);
        const info = await infoRes.json();
        const career = await careerRes.json();

        document.getElementById('modal-height').textContent = info.height || '—';
        document.getElementById('modal-weight').textContent = info.weight ? `${info.weight} lbs` : '—';
        document.getElementById('modal-country').textContent = info.country || '—';
        document.getElementById('modal-experience').textContent =
            info.experience !== undefined ? `${info.experience} yr${info.experience !== 1 ? 's' : ''}` : '—';

        if (Array.isArray(career) && career.length > 0) {
            const latest = career[career.length - 1];
            const fmt = (val, decimals = 1) =>
                val !== undefined && val !== null ? Number(val).toFixed(decimals) : '—';

            document.getElementById('cs-pts').textContent = fmt(latest.PTS);
            document.getElementById('cs-reb').textContent = fmt(latest.REB);
            document.getElementById('cs-ast').textContent = fmt(latest.AST);
            document.getElementById('cs-stl').textContent = fmt(latest.STL);
            document.getElementById('cs-blk').textContent = fmt(latest.BLK);
            document.getElementById('cs-fg').textContent = latest.FG_PCT
                ? `${(latest.FG_PCT * 100).toFixed(1)}%` : '—';
            document.getElementById('modal-career').style.display = 'block';
        }

        document.getElementById('modal-loading').style.display = 'none';
    } catch (e) {
        document.getElementById('modal-loading').textContent = 'Failed to load stats.';
    }
}

function closeModal(event) {
    if (event.target === document.getElementById('player-modal')) {
        closeModalBtn();
    }
}

function closeModalBtn() {
    document.getElementById('player-modal').classList.remove('active');
    document.body.style.overflow = '';
}

document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeModalBtn();
});

loadTeam();
