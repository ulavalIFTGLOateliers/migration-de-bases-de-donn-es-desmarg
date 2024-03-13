function migrate() {
    let statusElement = document.getElementById("migrate-status");
    statusElement.innerHTML = "Migration en cours..."

    fetch("/migrate", {
        method: "POST"
    }).then(function(response) {
        if (response.status === 200) {
            statusElement.innerHTML = "<p style='color:green'>Migration réussie. Cliquez sur rafraîchir pour voir le nouveau contenu de la BD.</p>"
        } else {
            statusElement.innerHTML = "<p style='color:red'>Échec. Une erreur est survenue lors de la migration. Référez-vous à l'erreur dans votre IDE.</p> <p style='color:#ff0000'>IMPORTANT: vous devez recréer la BD à nouveau.</p>"
        }
    })
}

function up()  {
    let statusElement = document.getElementById("up-status");
    statusElement.innerHTML = "Création en cours..."

    fetch("/up", {
        method: "POST"
    }).then(function(response) {
        if (response.status === 200) {
            statusElement.innerHTML = "<p style='color:green'>Création réussie. Cliquez sur rafraîchir pour voir le nouveau contenu de la BD.</p>"
        } else {
            statusElement.innerHTML = "<p style='color:red'>Échec. Une erreur est survenue lors de la création. Référez-vous à l'erreur dans votre IDE.</p>"
        }
    })
}

function rollback()  {
    let statusElement = document.getElementById("rollback-status");
    statusElement.innerHTML = "Migration arrière en cours..."

    fetch("/rollback", {
        method: "POST"
    }).then(function(response) {
        if (response.status === 200) {
            statusElement.innerHTML = "<p style='color:green'>Migration arrière réussie. Cliquez sur rafraîchir pour voir le nouveau contenu de la BD.</p>"
        } else {
            statusElement.innerHTML = "<p style='color:red'>Échec. Une erreur est survenue lors de la migration arrière. Référez-vous à l'erreur dans votre IDE.</p> <p style='color:red'>IMPORTANT: vous devez recréer la BD à nouveau.</p>"
        }
    })
}