<p align="center"><img src="https://raw.githubusercontent.com/EduWISP/.github/main/branding/eduwisp-mark.svg" alt="EduWISP" height="72"></p>

# eduwisp-users

**Core e identità** · *Core & Identity*

Tenant, utenti, ruoli, gruppi, autenticazione, autorizzazioni e multi-tenancy. È la base di tutti gli altri moduli.

> 🧪 **Stato: prototipo v0.** Organizzazioni (tenant), appartenenze con ruolo e isolamento dei dati tra istituti. La progettazione è nella [documentazione EduWISP](https://eduwisp.github.io/docs/architettura/architettura/).

🇬🇧 *Tenants, users, roles, groups, authentication, authorisation and multi-tenancy. The foundation of every other module. **Status: design phase**, no code yet. See the [design docs](https://eduwisp.github.io/docs/en/architecture/architecture/).*

## Documentazione / Documentation

- Progettazione / Design: <https://eduwisp.github.io/docs/architettura/architettura/>
- Mappa dei repository / Repository map: <https://eduwisp.github.io/docs/architettura/repository/>
- Documentazione del modulo / Module docs: [`docs/user/`](docs/user/) · [`docs/developer/`](docs/developer/)

## Cosa contiene il prototipo / What the prototype contains

- `Organization`: il tenant (istituto o rete di istituti).
- `Membership`: utente + organizzazione + ruolo (`school_admin`, `it_admin`, `teacher`).
- `OrganizationOwned`: modello astratto per i dati che appartengono a un tenant.
- `tenancy.organizations_for()` e `OrganizationScopedAdminMixin`: gli altri moduli li usano per mostrare a ciascuno **solo i dati della propria organizzazione**.
- Pie' di pagina dell'amministrazione con l'attribuzione obbligatoria «Basato su EduWISP» e il link al codice sorgente (AGPL, sezioni 7(b) e 13).

```bash
pip install -e ".[test]"
pytest
```

## Dipendenze / Dependencies

[`eduwisp-utils`](https://github.com/EduWISP/eduwisp-utils)

## Privacy

Dati personali previsti e regole: [PRIVACY.md](PRIVACY.md). Il rispetto della normativa su privacy e minori è un vincolo bloccante ([ADR-0008](https://eduwisp.github.io/docs/decisioni/0008-conformita-normativa/)).

## Responsabile del modulo / Module owner

Cerchiamo persone che vogliano prendere in carico questo modulo! Proponiti in [Discussions](https://github.com/EduWISP/docs/discussions). / *Want to own this module? Say hi in Discussions.*

## Contribuire / Contributing

Vedi [CONTRIBUTING](https://github.com/EduWISP/.github/blob/main/CONTRIBUTING.md) e il [Codice di condotta](https://github.com/EduWISP/.github/blob/main/CODE_OF_CONDUCT.md). **Mai dati personali reali** di studenti, famiglie o personale.

## Licenza / License

**AGPL-3.0-or-later**, con termini aggiuntivi di attribuzione e tutela del nome (sezione 7): vedi [LICENSE](LICENSE) e [NOTICE.md](NOTICE.md). Chi usa o modifica EduWISP deve sempre indicare «Basato su EduWISP» e non può usare il nome e il logo per versioni modificate. Licenza scelta secondo le [linee guida AgID](https://eduwisp.github.io/docs/decisioni/0006-licenza/) per il software usato via rete.

*AGPL-3.0-or-later with additional attribution and trademark terms (section 7): see LICENSE and NOTICE.md.*

I contributi richiedono il [DCO](https://github.com/EduWISP/.github/blob/main/CONTRIBUTING.md#dco) (`git commit -s`).
