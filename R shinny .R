library(shiny)
library(tidyverse)
library(readr)
library(plotly)
library(DT)
library(bslib)
library(forcats)

# -------------------- Données --------------------
data <- read_csv("data/filtered_most_important_problems_with_location.csv")

country_mapping <- c(
  `2` = "Angola", `3` = "Benin", `4` = "Botswana", `5` = "Burkina Faso",
  `6` = "Cameroon", `7` = "Cabo Verde", `8` = "Côte d'Ivoire", `9` = "Eswatini",
  `10` = "Ethiopia", `11` = "Gabon", `12` = "Gambia", `13` = "Ghana",
  `14` = "Guinea", `15` = "Kenya", `16` = "Lesotho", `17` = "Liberia",
  `18` = "Madagascar", `19` = "Malawi", `20` = "Mali", `21` = "Mauritius",
  `22` = "Morocco", `23` = "Mozambique", `24` = "Namibia", `25` = "Niger",
  `26` = "Nigeria", `27` = "São Tomé and Príncipe", `28` = "Senegal",
  `29` = "Sierra Leone", `30` = "South Africa", `31` = "Sudan",
  `32` = "Tanzania", `33` = "Togo", `34` = "Tunisia", `35` = "Uganda",
  `36` = "Zambia", `37` = "Zimbabwe"
)

q45_value_labels <- c(
  `-1` = "Missing", `9999` = "Don't know", `9998` = "Refused", `9995` = "Other", 
  `1680` = "Drug abuse", `1500` = "Pollution", `180` = "Internally displaced", 
  `34` = "COVID-19", `33` = "Climate change", `32` = "Agricultural marketing", 
  `31` = "Civil war", `30` = "War (international)", `29` = "Democracy/Political rights", 
  `28` = "Gender issues/Women's rights", `27` = "Discrimination/Inequality", 
  `26` = "Political instability/Divisions", `25` = "Political violence", 
  `24` = "Corruption", `23` = "Crime and security", `22` = "Sickness/Disease", 
  `21` = "AIDS", `20` = "Health", `19` = "Services (other)", `18` = "Orphans/Homeless children", 
  `17` = "Water supply", `16` = "Electricity", `15` = "Housing", `14` = "Education", 
  `13` = "Infrastructure/Roads", `12` = "Communications", `11` = "Transportation", 
  `10` = "Land", `9` = "Drought", `8` = "Food shortage/Famine", `7` = "Farming/Agriculture", 
  `6` = "Loans/Credit", `5` = "Rates and taxes", `4` = "Poverty/Destitution", 
  `3` = "Unemployment", `2` = "Wages, incomes, and salaries", `1` = "Management of the economy", 
  `0` = "Nothing/no problems"
)

titles <- list(
  "Q45PT1" = "First Most Important Problem",
  "Q45PT2" = "Second Most Important Problem",
  "Q45PT3" = "Third Most Important Problem"
)

problem_vars <- names(titles)

if (is.numeric(data$COUNTRY)) {
  data$COUNTRY <- as.character(country_mapping[as.character(data$COUNTRY)])
}
data$COUNTRY <- factor(data$COUNTRY)

for (var in problem_vars) {
  if (var %in% names(data)) {
    data[[var]] <- as.character(q45_value_labels[as.character(data[[var]])])
  }
}

# -------------------- Interface --------------------
my_theme <- bs_theme(
  version = 5,
  bootswatch = "flatly",
  primary = "#007BFF",
  base_font = font_google("Open Sans"),
  heading_font = font_google("Roboto Slab")
)

ui <- fluidPage(
  theme = my_theme,
  navbarPage(
    title = strong("AFROBAROMETER - DASHBOARD"),
    
    tabPanel("Dashboard",
             fluidRow(
               column(width = 2,
                      h4("Filters"),
                      selectInput("country", "Select a Country:", 
                                  choices = c("All", levels(data$COUNTRY)), selected = "All"),
                      checkboxGroupInput("problems", "Questions to display:", 
                                         choices = setNames(problem_vars, titles),
                                         selected = problem_vars)
               ),
               column(width = 10,
                      plotlyOutput("barplot", height = "900px", width = "100%")
               )
             )
    ),
    
    tabPanel("Country Comparison",
             fluidRow(
               column(width = 2,
                      h4("Compare Countries"),
                      selectInput("compare_countries", "Countries:", 
                                  choices = levels(data$COUNTRY), 
                                  selected = levels(data$COUNTRY)[1:3], multiple = TRUE),
                      selectInput("var_compare", "Select Question:", 
                                  choices = setNames(problem_vars, titles))
               ),
               column(width = 10,
                      plotlyOutput("compare_plot", height = "900px", width = "100%")
               )
             )
    ),
    
    tabPanel("Data Table", DTOutput("datatable")),
    
    tabPanel("About",
             h4("Project developed by Abdoul Wahid"),
             p("This Shiny app analyzes perceptions of most important problems across African countries using Afrobarometer data (Round 9)."),
             p("Data source: https://www.afrobarometer.org/")
    )
  )
)

# -------------------- Serveur --------------------
server <- function(input, output, session) {
  
  filtered_data <- reactive({
    df <- data
    if (input$country != "All") df <- df %>% filter(COUNTRY == input$country)
    df
  })
  
  output$barplot <- renderPlotly({
    req(input$problems)
    
    df_long <- filtered_data() %>%
      pivot_longer(cols = all_of(input$problems), names_to = "Question", values_to = "Response") %>%
      drop_na(Response) %>%
      group_by(Question, Response) %>%
      summarise(N = n(), .groups = "drop") %>%
      group_by(Question) %>%
      mutate(Percentage = N / sum(N) * 100) %>%
      ungroup()
    
    # TRI GLOBAL pour afficher les plus importants EN HAUT
    global_order <- df_long %>%
      group_by(Response) %>%
      summarise(TotalN = sum(N), .groups = "drop") %>%
      arrange(desc(TotalN)) %>%
      pull(Response) %>% rev()
    
    df_long <- df_long %>%
      mutate(Response = factor(Response, levels = global_order),
             Question = titles[Question] %>% unlist())
    
    p <- ggplot(df_long, aes(x = Percentage, y = Response, fill = Question)) +
      geom_bar(stat = "identity", position = "dodge") +
      labs(x = "% of responses", y = "", fill = "Question") +
      theme_minimal(base_size = 16) +
      theme(axis.text.x = element_text(size = 12),
            axis.text.y = element_text(size = 12))
    
    ggplotly(p) %>% layout(
      legend = list(
        orientation = "v", x = 1.1, y = 1, xanchor = "left", yanchor = "top", font = list(size = 13)
      ),
      margin = list(l = 100, r = 0, t = 20, b = 140),
      xaxis = list(domain = c(0, 0.85)),
      annotations = list(
        list(text = "<b>Distribution of Problems</b>",
             x = 0.5, y = -0.2, xref = "paper", yref = "paper",
             showarrow = FALSE, font = list(size = 20))
      )
    )
  })
  
  # ---------------- Country Comparison ----------------
  output$compare_plot <- renderPlotly({
    req(input$var_compare)
    
    df_comp <- data %>%
      filter(COUNTRY %in% input$compare_countries) %>%
      group_by(COUNTRY, Response = !!sym(input$var_compare)) %>%
      summarise(N = n(), .groups = "drop") %>%
      group_by(COUNTRY) %>%
      mutate(Percentage = N / sum(N) * 100) %>%
      ungroup() %>%
      mutate(Response = fct_reorder(Response, Percentage, .desc = TRUE))
    
    p <- ggplot(df_comp, aes(x = Percentage, y = Response, fill = COUNTRY)) +
      geom_bar(stat = "identity", position = "dodge") +
      labs(x = "% of responses", y = "", fill = "Country") +
      theme_minimal(base_size = 15) +
      theme(axis.text.x = element_text(size = 12),
            axis.text.y = element_text(size = 12))
    
    ggplotly(p) %>% layout(
      legend = list(
        orientation = "v",
        x = 0.9,  # Légende plus proche
        y = 1,
        xanchor = "left",
        yanchor = "top",
        font = list(size = 13)
      ),
      margin = list(l = 100, r = 0, t = 20, b = 140),
      xaxis = list(domain = c(0, 0.93)),  # Maintenant 93% de largeur
      annotations = list(
        list(
          text = "<b>Distribution of Problems</b>",
          x = 0.5, y = -0.2,
          xref = "paper", yref = "paper",
          showarrow = FALSE, font = list(size = 20))
      )
    )
    
  })
  
  output$datatable <- renderDT({
    datatable(data, options = list(pageLength = 10))
  })
}

# -------------------- Lancement --------------------
shinyApp(ui, server)
