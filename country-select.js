// ISO 3166-1 countries and territories; English display names. United States first.
// Keep the matching Apps Script allowlist in sync (checked by test_country_registration.cjs).
var COURSE_COUNTRIES = [
  "United States",
  "Afghanistan",
  "Åland Islands",
  "Albania",
  "Algeria",
  "American Samoa",
  "Andorra",
  "Angola",
  "Anguilla",
  "Antarctica",
  "Antigua & Barbuda",
  "Argentina",
  "Armenia",
  "Aruba",
  "Australia",
  "Austria",
  "Azerbaijan",
  "Bahamas",
  "Bahrain",
  "Bangladesh",
  "Barbados",
  "Belarus",
  "Belgium",
  "Belize",
  "Benin",
  "Bermuda",
  "Bhutan",
  "Bolivia",
  "Bosnia & Herzegovina",
  "Botswana",
  "Bouvet Island",
  "Brazil",
  "British Indian Ocean Territory",
  "British Virgin Islands",
  "Brunei",
  "Bulgaria",
  "Burkina Faso",
  "Burundi",
  "Cambodia",
  "Cameroon",
  "Canada",
  "Cape Verde",
  "Caribbean Netherlands",
  "Cayman Islands",
  "Central African Republic",
  "Chad",
  "Chile",
  "China",
  "Christmas Island",
  "Cocos (Keeling) Islands",
  "Colombia",
  "Comoros",
  "Congo - Brazzaville",
  "Congo - Kinshasa",
  "Cook Islands",
  "Costa Rica",
  "Côte d’Ivoire",
  "Croatia",
  "Cuba",
  "Curaçao",
  "Cyprus",
  "Czechia",
  "Denmark",
  "Djibouti",
  "Dominica",
  "Dominican Republic",
  "Ecuador",
  "Egypt",
  "El Salvador",
  "Equatorial Guinea",
  "Eritrea",
  "Estonia",
  "Eswatini",
  "Ethiopia",
  "Falkland Islands",
  "Faroe Islands",
  "Fiji",
  "Finland",
  "France",
  "French Guiana",
  "French Polynesia",
  "French Southern Territories",
  "Gabon",
  "Gambia",
  "Georgia",
  "Germany",
  "Ghana",
  "Gibraltar",
  "Greece",
  "Greenland",
  "Grenada",
  "Guadeloupe",
  "Guam",
  "Guatemala",
  "Guernsey",
  "Guinea",
  "Guinea-Bissau",
  "Guyana",
  "Haiti",
  "Heard & McDonald Islands",
  "Honduras",
  "Hong Kong SAR China",
  "Hungary",
  "Iceland",
  "India",
  "Indonesia",
  "Iran",
  "Iraq",
  "Ireland",
  "Isle of Man",
  "Israel",
  "Italy",
  "Jamaica",
  "Japan",
  "Jersey",
  "Jordan",
  "Kazakhstan",
  "Kenya",
  "Kiribati",
  "Kuwait",
  "Kyrgyzstan",
  "Laos",
  "Latvia",
  "Lebanon",
  "Lesotho",
  "Liberia",
  "Libya",
  "Liechtenstein",
  "Lithuania",
  "Luxembourg",
  "Macao SAR China",
  "Madagascar",
  "Malawi",
  "Malaysia",
  "Maldives",
  "Mali",
  "Malta",
  "Marshall Islands",
  "Martinique",
  "Mauritania",
  "Mauritius",
  "Mayotte",
  "Mexico",
  "Micronesia",
  "Moldova",
  "Monaco",
  "Mongolia",
  "Montenegro",
  "Montserrat",
  "Morocco",
  "Mozambique",
  "Myanmar (Burma)",
  "Namibia",
  "Nauru",
  "Nepal",
  "Netherlands",
  "New Caledonia",
  "New Zealand",
  "Nicaragua",
  "Niger",
  "Nigeria",
  "Niue",
  "Norfolk Island",
  "North Korea",
  "North Macedonia",
  "Northern Mariana Islands",
  "Norway",
  "Oman",
  "Pakistan",
  "Palau",
  "Palestinian Territories",
  "Panama",
  "Papua New Guinea",
  "Paraguay",
  "Peru",
  "Philippines",
  "Pitcairn Islands",
  "Poland",
  "Portugal",
  "Puerto Rico",
  "Qatar",
  "Réunion",
  "Romania",
  "Russia",
  "Rwanda",
  "Samoa",
  "San Marino",
  "São Tomé & Príncipe",
  "Saudi Arabia",
  "Senegal",
  "Serbia",
  "Seychelles",
  "Sierra Leone",
  "Singapore",
  "Sint Maarten",
  "Slovakia",
  "Slovenia",
  "Solomon Islands",
  "Somalia",
  "South Africa",
  "South Georgia & South Sandwich Islands",
  "South Korea",
  "South Sudan",
  "Spain",
  "Sri Lanka",
  "St. Barthélemy",
  "St. Helena",
  "St. Kitts & Nevis",
  "St. Lucia",
  "St. Martin",
  "St. Pierre & Miquelon",
  "St. Vincent & Grenadines",
  "Sudan",
  "Suriname",
  "Svalbard & Jan Mayen",
  "Sweden",
  "Switzerland",
  "Syria",
  "Taiwan",
  "Tajikistan",
  "Tanzania",
  "Thailand",
  "Timor-Leste",
  "Togo",
  "Tokelau",
  "Tonga",
  "Trinidad & Tobago",
  "Tunisia",
  "Türkiye",
  "Turkmenistan",
  "Turks & Caicos Islands",
  "Tuvalu",
  "U.S. Outlying Islands",
  "U.S. Virgin Islands",
  "Uganda",
  "Ukraine",
  "United Arab Emirates",
  "United Kingdom",
  "Uruguay",
  "Uzbekistan",
  "Vanuatu",
  "Vatican City",
  "Venezuela",
  "Vietnam",
  "Wallis & Futuna",
  "Western Sahara",
  "Yemen",
  "Zambia",
  "Zimbabwe"
];

function CountrySelect(props) {
  var E = React.createElement;
  var q = React.useState(props.value || ""), query = q[0], setQuery = q[1];
  var o = React.useState(false), open = o[0], setOpen = o[1];
  var a = React.useState(-1), active = a[0], setActive = a[1];
  var normalize = function(value) { return value.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase(); };
  var search = query === props.value ? "" : normalize(query.trim());
  var matches = COURSE_COUNTRIES.filter(function(name) { return normalize(name).indexOf(search) !== -1; });
  var optionId = function(name) { return "gate-country-option-" + COURSE_COUNTRIES.indexOf(name); };
  var choose = function(name) {
    props.onChange(name);
    setQuery(name);
    setOpen(false);
    setActive(-1);
  };
  React.useEffect(function() {
    if (!open || active < 0 || !matches[active]) return;
    var option = document.getElementById(optionId(matches[active]));
    if (option) option.scrollIntoView({ block: "nearest" });
  }, [open, active, query]);
  return E("div", { className: "gate-country gate-span2", onBlur: function(event) {
    if (!event.currentTarget.contains(event.relatedTarget)) {
      setOpen(false);
      setActive(-1);
      setQuery(props.value || "");
    }
  } },
    E("div", { className: "gate-country-control" },
      E("input", {
        type: "text", role: "combobox", className: "gate-field", value: query,
        placeholder: "Select your country", "aria-label": "Country", "aria-required": true,
        "aria-expanded": open, "aria-controls": "gate-country-list", "aria-autocomplete": "list",
        "aria-activedescendant": open && active >= 0 && matches[active] ? optionId(matches[active]) : undefined,
        autoComplete: "off", spellCheck: false, required: true,
        onFocus: function() { setOpen(true); },
        onClick: function() { setOpen(true); },
        onChange: function(event) {
          setQuery(event.target.value);
          props.onChange(""); // Typed text is never a selection, even if it matches a label.
          setOpen(true);
          setActive(-1);
        },
        onKeyDown: function(event) {
          if (event.key === "ArrowDown" || event.key === "ArrowUp") {
            event.preventDefault();
            setOpen(true);
            setActive(function(previous) {
              if (!matches.length) return -1;
              if (!open || previous < 0) return event.key === "ArrowDown" ? 0 : matches.length - 1;
              return Math.max(0, Math.min(matches.length - 1, previous + (event.key === "ArrowDown" ? 1 : -1)));
            });
          } else if (event.key === "Enter" && open) {
            event.preventDefault();
            if (matches[active >= 0 ? active : 0]) choose(matches[active >= 0 ? active : 0]);
          } else if (event.key === "Escape" && open) {
            event.preventDefault();
            setOpen(false);
            setActive(-1);
            setQuery(props.value || "");
          } else if (open && (event.key === "Home" || event.key === "End") && active >= 0) {
            event.preventDefault();
            setActive(event.key === "Home" ? 0 : matches.length - 1);
          }
        }
      })),
    open ? E("div", { className: "gate-country-menu" },
      E("ul", { id: "gate-country-list", role: "listbox", "aria-label": "Countries", className: "gate-country-list" },
        matches.map(function(name, index) {
          return E("li", { key: name, id: optionId(name), role: "option", "aria-selected": props.value === name,
            className: "gate-country-option" + (active === index ? " is-active" : ""),
            onMouseDown: function(event) { event.preventDefault(); },
            onClick: function() { choose(name); }
          }, name);
        })),
      !matches.length ? E("p", { className: "gate-country-empty", role: "status" }, "No matching countries. Try another search.") : null
    ) : null);
}
