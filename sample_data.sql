USE db_akademik;

-- ============================================
-- Program Studi
-- ============================================

INSERT INTO program_studi (nama_prodi)

VALUES

('Informatika'),

('Sistem Informasi'),

('Teknik Komputer');

-- ============================================
-- Mahasiswa
-- ============================================

INSERT INTO mahasiswa

VALUES

('2211001','Andi Saputra','andi@gmail.com',1),

('2211002','Budi Santoso','budi@gmail.com',1),

('2211003','Citra Lestari','citra@gmail.com',2),

('2211004','Dinda Putri','dinda@gmail.com',3);

-- ============================================
-- Mata Kuliah
-- ============================================

INSERT INTO mata_kuliah

VALUES

('IF101','Algoritma',3),

('IF102','Basis Data',3),

('IF103','Pemrograman Web',3),

('IF104','Jaringan Komputer',2),

('IF105','Kecerdasan Buatan',3);

-- ============================================
-- KRS
-- ============================================

INSERT INTO krs(nim,kode)

VALUES

('2211001','IF101'),

('2211001','IF102'),

('2211001','IF103'),

('2211002','IF101'),

('2211002','IF104'),

('2211003','IF102'),

('2211003','IF103'),

('2211004','IF105');