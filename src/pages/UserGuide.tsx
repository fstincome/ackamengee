import { BookOpen, Download, ArrowUpRight } from "lucide-react";
import { Button } from "@/components/ui/button";
import guide from "@/content/user-guide.json";

export default function UserGuide() {
  return (
    <div className="mx-auto max-w-5xl">
      <div className="page-header flex flex-col items-start justify-between gap-5 sm:flex-row sm:items-center">
        <div>
          <p className="mb-2 text-xs font-semibold uppercase text-primary">{guide.organization} · Staff handbook</p>
          <h1 className="page-title tracking-normal">{guide.title}</h1>
          <p className="page-subtitle max-w-lg">{guide.subtitle}</p>
        </div>
        <Button asChild className="shrink-0">
          <a href="/downloads/american-corner-kamenge-user-guide.pdf" download="American-Corner-Kamenge-User-Guide.pdf">
            <Download aria-hidden="true" /> Download PDF
          </a>
        </Button>
      </div>

      <div className="grid gap-10 lg:grid-cols-[220px_minmax(0,1fr)]">
        <nav aria-label="Guide contents" className="self-start lg:sticky lg:top-0">
          <p className="mb-4 flex items-center gap-2 text-sm font-semibold text-foreground"><BookOpen className="h-4 w-4 text-primary" /> Contents</p>
          <ol className="space-y-1 border-l border-border">
            {guide.sections.map((section, index) => (
              <li key={section.id}>
                <a href={`#${section.id}`} className="flex gap-3 py-2 pl-4 text-sm text-muted-foreground transition-colors hover:text-primary">
                  <span className="font-mono text-xs text-primary">{String(index + 1).padStart(2, "0")}</span>
                  <span>{section.title}</span>
                </a>
              </li>
            ))}
          </ol>
          <p className="mt-4 text-xs text-muted-foreground">Edition · {guide.edition}</p>
        </nav>

        <div className="min-w-0">
          {guide.sections.map((section, index) => (
            <section id={section.id} key={section.id} aria-labelledby={`${section.id}-title`} className="scroll-mt-6 border-b border-border pb-8 mb-8 last:mb-0">
              <p className="mb-2 font-mono text-xs font-semibold text-accent">{String(index + 1).padStart(2, "0")}</p>
              <h2 id={`${section.id}-title`} className="text-2xl tracking-normal text-foreground">{section.title}</h2>
              <p className="mt-2 mb-5 text-sm leading-relaxed text-muted-foreground">{section.summary}</p>
              <ol className="space-y-4">
                {section.steps.map((step, stepIndex) => (
                  <li key={stepIndex} className="flex gap-3 text-sm leading-6 text-foreground">
                    <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-secondary text-xs font-semibold text-secondary-foreground">{stepIndex + 1}</span>
                    <span>{step}</span>
                  </li>
                ))}
              </ol>
              <div className="mt-5 border-l-2 border-primary bg-muted/50 px-4 py-3 text-sm leading-6 text-muted-foreground">
                <p className="font-semibold text-foreground">Good to know</p>
                <p>{section.note}</p>
              </div>
            </section>
          ))}
          <a href="#getting-started" className="inline-flex items-center gap-2 text-sm font-medium text-primary hover:underline">Back to the beginning <ArrowUpRight className="h-4 w-4" /></a>
        </div>
      </div>
    </div>
  );
}