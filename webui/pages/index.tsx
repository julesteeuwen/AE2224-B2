import { Link } from "@nextui-org/link";
import { Snippet } from "@nextui-org/snippet";
import { Code } from "@nextui-org/code";
import { Select, SelectItem } from "@nextui-org/react"
import { button as buttonStyles } from "@nextui-org/theme";
import { siteConfig } from "@/config/site";
import { title, subtitle } from "@/components/primitives";
import { GithubIcon } from "@/components/icons";
import DefaultLayout from "@/layouts/default";
import {Tabs, Tab, Card, CardBody, CardHeader} from "@nextui-org/react";
import { ANSPChart } from "@/components/anspchart";
import { useState, useEffect, useMemo } from "react";
import { Selection } from "@nextui-org/react";


export default function IndexPage() {
	const ansps = ['ANS CR', 'ARMATS', 'Albcontrol', 'Austro Control', 'Avinor (Continental)', 'BULATSA', 'Belgocontrol', 'Croatia Control', 'DCAC Cyprus', 'DFS', 'DHMI', 'DSNA', 'EANS', 'ENAIRE', 'ENAV', 'Finavia', 'HCAA', 'HungaroControl', 'IAA', 'LFV', 'LGS', 'LPS', 'LVNL', 'M-NAV', 'MATS', 'MUAC', 'MoldATSA', 'NATS (Continental)', 'NAV Portugal (Continental)', 'NAVIAIR', 'Oro Navigacija', 'PANSA', 'ROMATSA', 'SMATSA', 'Sakaeronavigatsia', 'Skyguide', 'Slovenia Control', 'UkSATSE']

	const [SelectedANSPs, setSelectedANSPs] = useState(new Set<string>([ansps[0]]));

	const handleSelectionChange = (keys: Selection) => {
		setSelectedANSPs(new Set<string>(Array.from(keys).map(key => key.toString())));
	};


	let tabs = [
		{
			id: "data",
			label: "Data",
			content: ";)"
		},
		{
			id: "vis",
			label: "Visualisation",
			content: <ANSPChart ansps={Array.from(SelectedANSPs)}></ANSPChart>
		},
		{
		id: "music",
		label: "Forecasting",
		content: "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur."
		},
		{
		id: "videos",
		label: "Videos",
		content: "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
		}
	];
	
	return (
		<DefaultLayout>
			<section className="flex flex-col items-center justify-center gap-4 py-8 md:py-10">
				
				<Select
					label="ANSPs"
					placeholder="Select the ANSPs"
					selectionMode="multiple"
					className="max-w-xs"
					selectedKeys={SelectedANSPs}
					onSelectionChange={handleSelectionChange}
				>
					{ansps.map((ansp) => (
						<SelectItem key={ansp} value={ansp}>
							{ansp}
						</SelectItem>
					))}
				</Select>
				<p className="text-small text-default-500">Selected: {Array.from(SelectedANSPs).join(", ")}</p>
				<Tabs aria-label="Dynamic tabs" items={tabs}>
					{(item) => (
					<Tab key={item.id} title={item.label}>
						<Card>
						<CardBody>
							{item.content}
						</CardBody>
						</Card>  
					</Tab>
					)}
				</Tabs>
				<div className="inline-block max-w-lg text-center justify-center">
					<h1 className={title()}>Complexity score analysis and forecasting&nbsp;</h1>
					<h1 className={title({ color: "violet" })}>AE2224-B2&nbsp;</h1>
					<br />
					<h1 className={title()}>
						
					</h1>
					<h4 className={subtitle({ class: "mt-4" })}>
						Beautiful, fast and modern React UI library.
					</h4>
				</div>

				<div className="flex gap-3">
					<Link
						isExternal
						href={siteConfig.links.docs}
						className={buttonStyles({
							color: "primary",
							radius: "full",
							variant: "shadow",
						})}
					>
						Documentation
					</Link>
					<Link
						isExternal
						className={buttonStyles({ variant: "bordered", radius: "full" })}
						href={siteConfig.links.github}
					>
						<GithubIcon size={20} />
						GitHub
					</Link>
				</div>
			</section>
		</DefaultLayout>
	);
}
