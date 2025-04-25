-- CreateTable
CREATE TABLE `clubes` (
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    `nome` VARCHAR(40) NOT NULL,
    `estado` VARCHAR(2) NOT NULL,

    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
CREATE TABLE `jogadores` (
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    `nome` VARCHAR(40) NOT NULL,
    `datanasc` DATETIME(3) NOT NULL,
    `salario` DECIMAL(10, 2) NOT NULL,
    `nacionalidade` VARCHAR(20) NOT NULL,
    `clubeId` INTEGER NOT NULL,

    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- AddForeignKey
ALTER TABLE `jogadores` ADD CONSTRAINT `jogadores_clubeId_fkey` FOREIGN KEY (`clubeId`) REFERENCES `clubes`(`id`) ON DELETE RESTRICT ON UPDATE CASCADE;
