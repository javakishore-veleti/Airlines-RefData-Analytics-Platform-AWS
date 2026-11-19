# D5 — Portal UI system

**Stories:** #62 (record), #40 (Admin shell), #46 (Intelligence shell)  
**Date:** 2026-11-19  
**Status:** Decided

## Stack

- Angular apps for Admin and Intelligence
- **PrimeNG Aura/Lara light** as the primary component library
- Bootstrap 5 Sass **grid/spacing only**, with `$gray-*` remapped to ARFD navy/ice tokens (no stock Bootstrap look)
- **Lucide** icons; favicon + brand mark in the top bar
- **Plus Jakarta Sans** typography

## Chrome

- Top main menu bar (deep navy)
- Collapsible left nav (navy, sky active state)
- Ice-blue canvas `#F4F8FB`, white content surfaces, powder-blue borders
- Signup / signin via AccountService-API
- Admin: User Management menu → AccountService CRUD

## Anti-patterns

- Pure black / sterile gray UI
- Academic “bootstrap default” gray admin templates
- Purple gradient / glow SaaS clichés
- Mixing full Bootstrap components with PrimeNG without a single token source
