import { BASE_API_URL } from '#lib/utils/constants.js';
import { m } from '#paraglide/messages.js';
import type { PageServerLoad } from './$types';

export const load = (async ({ fetch }) => {
	const res = await fetch(`${BASE_API_URL}/finreg/financial-institutions/overview/`);
	const overview = res.ok ? await res.json() : null;
	return { overview, title: m.finregOverview() };
}) satisfies PageServerLoad;
