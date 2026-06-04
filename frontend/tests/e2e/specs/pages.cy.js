describe('Page smoke tests', () => {
  const pages = [
    { path: '/surat-masuk', title: 'Surat Masuk', tableHeaders: ['No', 'No. Surat', 'Asal Surat', 'Perihal', 'Tanggal', 'Dokumen', 'Aksi'] },
    { path: '/surat-keluar', title: 'Surat Keluar', tableHeaders: ['No', 'No. Surat', 'Tujuan Surat', 'Perihal', 'Tanggal', 'Dokumen', 'Aksi'] },
    { path: '/disposisi', title: 'Disposisi', tableHeaders: ['No', 'ID Surat Masuk', 'Diteruskan Kepada', 'Instruksi / Catatan', 'Tanggal Disposisi', 'Status', 'Aksi'] },
    { path: '/arsip', title: 'Arsip', tableHeaders: ['No', 'No. Surat', 'Jenis', 'Asal / Tujuan', 'Perihal', 'Tanggal Arsip', 'Aksi'] },
  ];

  pages.forEach((page) => {
    it(`should load ${page.title} page`, () => {
      cy.visit(page.path, {
        onBeforeLoad(win) {
          win.localStorage.setItem('token', 'test-token');
        },
      });
      cy.url().should('include', page.path);
      cy.contains('.page-title, ion-title, h1, h2, h3', page.title).should('be.visible');
      cy.get('ion-content').should('exist');
      page.tableHeaders.forEach((header) => {
        cy.get('table').contains(header).should('exist');
      });

      cy.contains('button', /tambah|add/i).should('not.exist');
    });
  });
});
