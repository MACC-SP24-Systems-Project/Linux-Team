#include <curl/curl.h>
#include <string>

int main(int args, char *argc[])
{
	CURL *curl;
	CURLcode res;
	curl = curl_easy_init();
	if (curl)
	{
		curl_easy_setopt(curl, CURLOPT_CUSTOMREQUEST, "POST");
		curl_easy_setopt(curl, CURLOPT_URL, "https://my.macc.edu/ICS/webserviceproxy/exi/rest/studentregistration/pagedsectiondataforsearch?Id=57&IdNumber=-1&YearCode=2023&TermCode=SP");
		curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 1L);
		curl_easy_setopt(curl, CURLOPT_DEFAULT_PROTOCOL, "https");
		struct curl_slist *headers = NULL;
		headers = curl_slist_append(headers, "authority: my.macc.edu");
		headers = curl_slist_append(headers, "accept: text/html, */*; q=0.01");
		headers = curl_slist_append(headers, "accept-language: en-US,en;q=0.9");
		headers = curl_slist_append(headers, "content-type: application/json");
		headers = curl_slist_append(headers, "origin: https://my.macc.edu");
		headers = curl_slist_append(headers, "referer: https://my.macc.edu/ICS/Course_Offerings.jnz?portlet=Course_Search&screen=StudentRegistrationPortlet_CourseSearchView&screenType=next");
		headers = curl_slist_append(headers, "Cookie: .sessionheartbeat=2/29/2024 10:44:41 AM; ASP.NET_SessionId=3zb0wk1dkraxfzyik1d2iunw");
		curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
		const char *data = "{\"pageState\":{\"enabled\":true,\"keywordFilter\":\"\",\"quickFilters\":[],\"sortColumn\":\"\",\"sortAscending\":true,\"currentPage\":0,\"pageSize\":15,\"showingAll\":false,\"selectedAll\":false,\"excludedFromSelection\":[],\"includedInSelection\":[],\"advancedFilters\":[{\"name\":\"courseCode\",\"value\":\"\"},{\"name\":\"courseCodeType\",\"value\":\"0\"},{\"name\":\"courseTitle\",\"value\":\"\"},{\"name\":\"courseTitleType\",\"value\":\"0\"},{\"name\":\"requestNumber\",\"value\":\"\"},{\"name\":\"instructorIds\",\"value\":\"\"},{\"name\":\"departmentIds\",\"value\":\"\"},{\"name\":\"locationIds\",\"value\":\"\"},{\"name\":\"competencyIds\",\"value\":\"\"},{\"name\":\"beginsAfter\",\"value\":\"\"},{\"name\":\"beginsBefore\",\"value\":\"\"},{\"name\":\"instructionalMethods\",\"value\":\"\"},{\"name\":\"sectionStatus\",\"value\":\"\"},{\"name\":\"startCourseNumRange\",\"value\":\"\"},{\"name\":\"endCourseNumRange\",\"value\":\"\"},{\"name\":\"division\",\"value\":\"\"},{\"name\":\"place\",\"value\":\"\"},{\"name\":\"subterm\",\"value\":\"\"},{\"name\":\"meetsOnDays\",\"value\":\"0,0,0,0,0,0,0\"}],\"totalRows\":15,\"filteredRows\":845,\"quickFilterCounts\":null}}";
		curl_easy_setopt(curl, CURLOPT_POSTFIELDS, data);
		res = curl_easy_perform(curl);
		curl_slist_free_all(headers);
	}
	curl_easy_cleanup(curl);

	return 0;
}