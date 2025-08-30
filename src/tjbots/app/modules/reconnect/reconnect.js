$(document).on('shiny:connected', function () {
    // Indicate that this shiny app supports reconnection
    if (window.Shiny && Shiny.shinyapp) {
        Shiny.shinyapp.$allowReconnect = true;
    }
});
