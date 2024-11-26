/*
  Warnings:

  - A unique constraint covering the columns `[type_rol]` on the table `Rol` will be added. If there are existing duplicate values, this will fail.

*/
-- AlterTable
ALTER TABLE "Rol" ALTER COLUMN "type_rol" DROP DEFAULT;

-- CreateIndex
CREATE UNIQUE INDEX "Rol_type_rol_key" ON "Rol"("type_rol");

-- Insert Data
INSERT INTO "Rol"(id,type_rol)
VALUES
  (gen_random_uuid (),'User'),
  (gen_random_uuid (),'Admin')
ON CONFLICT (id) DO NOTHING;