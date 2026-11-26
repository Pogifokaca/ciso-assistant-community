<script lang="ts">
	import type { PageData } from './$types';
	import { safeTranslate } from '#lib/utils/i18n.js';
	import { m } from '#paraglide/messages.js';

	interface Props {
		data: PageData;
	}

	let { data }: Props = $props();

	const o = $derived(data.overview ?? {});
	const counts = $derived(o.counts ?? {});

	const kpis = $derived([
		{
			label: m.financialInstitutions(),
			value: counts.institutions ?? 0,
			href: '/financial-institutions',
			icon: 'fa-building-columns',
			tone: 'text-primary-600'
		},
		{
			label: m.regulators(),
			value: counts.regulators ?? 0,
			href: '/regulators',
			icon: 'fa-landmark',
			tone: 'text-primary-600'
		},
		{
			label: m.regulatoryObligations(),
			value: counts.obligations ?? 0,
			href: '/regulatory-obligations',
			icon: 'fa-scale-balanced',
			tone: 'text-primary-600'
		},
		{
			label: m.openReports(),
			value: counts.open_reports ?? 0,
			sub: counts.overdue_reports
				? m.overdueCount({ count: counts.overdue_reports })
				: undefined,
			href: '/regulatory-reports',
			icon: 'fa-file-export',
			tone: counts.overdue_reports ? 'text-error-600' : 'text-primary-600'
		},
		{
			label: m.openSupervisoryFindings(),
			value: counts.open_findings ?? 0,
			sub: counts.overdue_findings
				? m.overdueCount({ count: counts.overdue_findings })
				: undefined,
			href: '/supervisory-findings',
			icon: 'fa-magnifying-glass-chart',
			tone: counts.overdue_findings ? 'text-error-600' : 'text-primary-600'
		}
	]);

	const STATUS_COLORS: Record<string, string> = {
		compliant: 'bg-success-500',
		partially_compliant: 'bg-warning-500',
		non_compliant: 'bg-error-500',
		not_applicable: 'bg-surface-400',
		not_assessed: 'bg-surface-300',
		planned: 'bg-surface-300',
		in_preparation: 'bg-primary-300',
		in_review: 'bg-primary-500',
		submitted: 'bg-success-400',
		accepted: 'bg-success-600',
		returned: 'bg-error-500',
		low: 'bg-success-400',
		medium: 'bg-warning-400',
		high: 'bg-error-400',
		critical: 'bg-error-700'
	};

	function rows(map: Record<string, number> | undefined) {
		const entries = Object.entries(map ?? {}).sort((a, b) => b[1] - a[1]);
		const total = entries.reduce((sum, [, n]) => sum + n, 0);
		return entries.map(([key, n]) => ({ key, n, pct: total ? Math.round((n * 100) / total) : 0 }));
	}

	const panels = $derived([
		{
			title: m.institutionsByType(),
			rows: rows(o.institutions_by_type),
			link: (key: string) => `/financial-institutions?institution_type=${key}`
		},
		{
			title: m.obligationsByStatus(),
			rows: rows(o.obligations_by_status),
			link: (key: string) => `/regulatory-obligations?status=${key}`
		},
		{
			title: m.reportsByStatus(),
			rows: rows(o.reports_by_status),
			link: (key: string) => `/regulatory-reports?status=${key}`
		},
		{
			title: m.openFindingsBySeverity(),
			rows: rows(o.findings_by_severity),
			link: (key: string) => `/supervisory-findings?severity=${key}`
		}
	]);

	const today = new Date().toISOString().slice(0, 10);
</script>

<div class="p-4 space-y-6">
	{#if !data.overview}
		<p class="text-surface-600">{m.anErrorOccurred()}</p>
	{:else}
		<div class="grid grid-cols-2 md:grid-cols-3 xl:grid-cols-5 gap-4">
			{#each kpis as kpi}
				<a
					href={kpi.href}
					class="card bg-white dark:bg-surface-900 border border-surface-200-800 rounded-xl p-4 hover:shadow-md transition-shadow"
				>
					<div class="flex items-center justify-between">
						<span class="text-sm text-surface-600-400">{kpi.label}</span>
						<i class="fa-solid {kpi.icon} {kpi.tone}"></i>
					</div>
					<div class="mt-2 text-3xl font-semibold {kpi.tone}">{kpi.value}</div>
					{#if kpi.sub}
						<div class="text-xs text-error-600 mt-1">{kpi.sub}</div>
					{/if}
				</a>
			{/each}
		</div>

		<div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
			{#each panels as panel}
				<div class="card bg-white dark:bg-surface-900 border border-surface-200-800 rounded-xl p-4">
					<h3 class="font-semibold mb-3">{panel.title}</h3>
					{#if panel.rows.length === 0}
						<p class="text-sm text-surface-500">{m.noData()}</p>
					{:else}
						<ul class="space-y-2">
							{#each panel.rows as row}
								<li>
									<a href={panel.link(row.key)} class="block group">
										<div class="flex justify-between text-sm">
											<span class="group-hover:underline">{safeTranslate(row.key)}</span>
											<span class="text-surface-600-400">{row.n}</span>
										</div>
										<div class="h-2 rounded bg-surface-100-900 overflow-hidden">
											<div
												class="h-2 rounded {STATUS_COLORS[row.key] ?? 'bg-primary-500'}"
												style="width: {row.pct}%"
											></div>
										</div>
									</a>
								</li>
							{/each}
						</ul>
					{/if}
				</div>
			{/each}
		</div>

		<div class="card bg-white dark:bg-surface-900 border border-surface-200-800 rounded-xl p-4">
			<div class="flex items-center justify-between mb-3">
				<h3 class="font-semibold">{m.upcomingRegulatoryReports()}</h3>
				<a href="/regulatory-reports" class="text-sm text-primary-600 hover:underline"
					>{m.seeAll()}</a
				>
			</div>
			{#if (o.upcoming_reports ?? []).length === 0}
				<p class="text-sm text-surface-500">{m.noData()}</p>
			{:else}
				<table class="w-full text-sm">
					<thead>
						<tr class="text-left text-surface-600-400 border-b border-surface-200-800">
							<th class="py-2">{m.dueDate()}</th>
							<th>{m.name()}</th>
							<th>{m.financialInstitution()}</th>
							<th>{m.status()}</th>
						</tr>
					</thead>
					<tbody>
						{#each o.upcoming_reports as report}
							<tr class="border-b border-surface-100-900">
								<td class="py-2 {report.due_date < today ? 'text-error-600 font-semibold' : ''}">
									{report.due_date}
								</td>
								<td>
									<a href="/regulatory-reports/{report.id}" class="hover:underline">
										{report.ref_id ? `${report.ref_id} — ` : ''}{report.name}
									</a>
								</td>
								<td>{report.institution ?? '--'}</td>
								<td>{safeTranslate(report.status)}</td>
							</tr>
						{/each}
					</tbody>
				</table>
			{/if}
		</div>
	{/if}
</div>
