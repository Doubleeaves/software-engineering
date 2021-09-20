#include<bits/stdc++.h>
using namespace std;
string fileName="flight_information.txt";
string weekdays[]={" ","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"};
void showTheMessage(int i=0)
{  
   // " NO   MAX START   END    Take Off Time     Landing Time     Day    Status\n"
   char no[]="NO";
   char max[]="max";
   char start[]="START";
   char end[]="END";
   char take[]="Take Off Time";
   char land[]="Landing Time";
   char day[]="Day";
   char status[]="Status";
   if(i==0)
   printf("%-10s%-5s%-10s%-10s%-20s%-20s%-10s%-10s\n",no,max,start,end,take,land,day,status);
   else printf("%-10s%-5s%-10s%-10s%-20s%-20s%-10s\n",no,max,start,end,take,land,day);
}
class Flight
{   
    string flightNumber;
    int maxMember;
    string endStation;
    string startStation;
    string takeOffTime;
    string landingTime;
    string weekday;
    string status;
    int bookedSit;
    public:
    friend ostream &operator<<(ostream &out,const Flight &flight)
    {
      // " NO   MAX START   END    Take Off Time     Landing Time     Day    Status\n"
      printf("%-10s%-5d%-10s%-10s%-20s%-20s%-10s%-10s",flight.flightNumber.c_str(),flight.maxMember,flight.startStation.c_str(),
      flight.endStation.c_str(),flight.takeOffTime.c_str(),flight.landingTime.c_str(),flight.weekday.c_str(),flight.status.c_str());
      return out;
    }
    friend istream &operator>>(istream &is,Flight &flight)
    {
      is>>flight.flightNumber>>flight.maxMember>>flight.startStation>>flight.endStation>>flight.takeOffTime>>flight.landingTime>>flight.weekday;
      return is;
    }
    friend ofstream &operator<<(ofstream &out,const Flight &flight)
    {
      out<<flight.flightNumber<<" "<<flight.maxMember<<" "<<flight.startStation<<" "<<flight.endStation<<" "<<flight.takeOffTime<<" "<<flight.landingTime<<" "<<flight.weekday<<" ";
      if(flight.bookedSit==flight.maxMember)out<<flight.status;
      else out<<flight.status;
      out<<" "<<flight.bookedSit;
      return out;
    }
    friend ifstream &operator>>(ifstream &is,Flight &flight)
    {
      is>>flight.flightNumber>>flight.maxMember>>flight.startStation>>flight.endStation>>flight.takeOffTime>>flight.landingTime>>flight.weekday>>flight.status>>flight.bookedSit;
      return is;
    }
    bool operator==(const Flight &other)
    {
      if(other.flightNumber!=flightNumber)return 0;
      if(other.maxMember!=maxMember)return 0;
      if(other.startStation!=startStation)return 0;
      if(other.endStation!=endStation)return 0;
      if(other.takeOffTime!=takeOffTime)return 0;
      if(other.weekday!=weekday)return 0;
      if(other.landingTime!=landingTime)return 0;
      if(other.bookedSit!=bookedSit)return 0;
      return 1;
    }
    Flight( string flightNumber,int maxMember,string takeOff,string lnading,string weekday,string endStation,string startStation)
    {
      this->flightNumber=flightNumber;
      this->maxMember=maxMember;
      this->takeOffTime=takeOff;
      this->landingTime=lnading;
      this->weekday=weekday;
      this->endStation=endStation;
      this->startStation=startStation;
      this->bookedSit=0;
      this->status="Bookable";
    }
    Flight()
    {
      status="Bookable";
      bookedSit=0;
    }
    void setFlightNumber(string flightnumber)
    {
      this->flightNumber=flightnumber;
    }
    void setMaxMember(int maxMember)
    {
      this->maxMember=maxMember;
    }
    void setEndStation(string endStation)
    {
      this->endStation=endStation;
    }
    void setStartStation(string startStation)
    {
      this->startStation=startStation;
    }
    void settakeOffTime(string time)
    {
      this->takeOffTime=time;
    }
    void setLandingTime(string time)
    {
      this->landingTime=time;
    }
    void setWeekday(string weekday)
    {
      this->weekday=weekday;
    }
    void setStatus(string status)
    {
      this->status=status;
    }
    string getStatus()
    {
      return this->status;
    }
    string getFlightNumber()
    {
      return this->flightNumber;
      }
    int getMaxMember()
    {
      return this->maxMember;
    }
    string getEndStation()
    {
      return this->endStation;
    }
    string getStartStation()
    {
      return this->startStation;
    };
    string getTakeOffTime()
    {
      return this->takeOffTime;
    };
    string getLandingTime()
    {
      return this->landingTime;
    }
    string getWeekday()
    {
      return this->weekday;
    }
    bool isFull()
    {
      return maxMember==bookedSit;
    }
  friend void booking(Flight &f)
    {
      if(!f.isFull())
      { 
        cout<<"Booking successful!\n";
        ++f.bookedSit;
      }
      else cout<<"This air is full!\n";
      if(f.isFull())f.status="Full";
    }
  friend void refunding(Flight &f)
  { 

      f.bookedSit--;
      f.status="Bookable";
  }
};
class Passenger
{
  string username;
  string password;
  vector<Flight> bookedTicket;
  public:
  Passenger()=default;
  void setUsername(string username)
  {
    this->username=username;
  }
  void setPassword(string password)
  {
    this->password=password;
  }
  Passenger(string username,string password)
  {
    this->username=username;
    this->password=password;
    bookedTicket.clear();
  }
  bool isConflict(Flight flight)
  { 
    cout<<"use isConflict function\n";
    for(int i=0;i<bookedTicket.size();i++)
    {
      if(flight.getTakeOffTime()>=bookedTicket[i].getTakeOffTime()&&flight.getTakeOffTime()<=bookedTicket[i].getLandingTime())
      return 1;
      else if(flight.getLandingTime()>=bookedTicket[i].getTakeOffTime()&&flight.getLandingTime()<=bookedTicket[i].getLandingTime())
      return 1;
    }
    return 0;
  }
  void book(Flight &flight)
  {
   if(isConflict(flight))cout<<"You have another air in this time!\n";
   else 
   { 
     booking(flight);
     bookedTicket.push_back(flight);
   } 
  }
  void showMyTicket()
   {
     showTheMessage(1);
     for(auto i:bookedTicket)
     {
      printf("%-10s%-5d%-10s%-10s%-20s%-20s%-10s\n",i.getFlightNumber().c_str(),i.getMaxMember(),i.getStartStation().c_str(),
      i.getEndStation().c_str(),i.getTakeOffTime().c_str(),i.getLandingTime().c_str(),i.getWeekday().c_str());
     }
   }
  void refund(Flight &flight)
  {
    for(int i=0;i<bookedTicket.size();i++)
    {
      if(bookedTicket[i]==flight)
      {
        refunding(flight);
        bookedTicket.erase(bookedTicket.begin()+i);
        cout<<"Refunding success!\n";
        return;
      }
    }
    cout<<"Failed! You not booked this air!\n";
  }
};
class Menu
{ 
  map<string,Flight> flightmap;
  public:
  Menu()
  { 
    flightmap.clear();
    Flight f;
    ifstream in;
    in.open(fileName,ios::in);
    while(1)
    {
      in>>f;
      if(in.fail())break;
      flightmap[f.getFlightNumber()]=f;
    }
  }
  void mainMenu(Passenger passenger)
  { 
    temp3:cout<<"Welcom to new Nippori airport!\n";
    string username,password;
    cout<<"Please login:\n";
    cout<<"Your username:\n";
    cin>>username;
    cout<<"Your password:\n";
    cin>>password;
    passenger.setUsername(username);
    passenger.setPassword(password);
    if(username=="admin")
    {
      temp1:if(password=="123456")
      {
        admin();
        cout<<"Saving file....... System will restart!\n";
        goto temp3;
      }
      else 
      {
       cout<<"Error! Please input again!\n";
       cout<<"Your password:\n";
       cin>>password;
       goto temp1;
      }
    }
    else 
    { 
      functionMmenu(passenger);
    }

  }
  private:
  void functionMmenu(Passenger &passenger)
  { 
    string service="1";
    cout<<"The service code is:\n";
    cout<<"1------Find air by number\n";
    cout<<"2------Find air by endstation\n";
    cout<<"3------Book ticket\n";
    cout<<"4------Refund Ticket\n";
    cout<<"5------Show all air information\n";
    cout<<"6------Show your Tickets\n";
    cout<<"0------Exit system\n";
    while(atoi(service.c_str())!=0||service.size()>1){
    cout<<"Please input corresponding service code:\n";
    cin>>service;
    temp2: if(service.size()>1||isalpha(service[0]))service="10";
    switch(atoi(service.c_str()))
    {
      case 1:
      {
        cout<<"Please input the air number\n";
        string number;
        cin>>number;
        findByNumber(number);
        break;
      }
      case 2:
      {
        cout<<"Please input the ending station:\n";
        string station;
        cin>>station;
        findByEndStation(station);
        break;
      }
      case 3:
      {
        cout<<"Please input the flight number:\n";
        string number;
        cin>>number;
        if(number==flightmap[number].getFlightNumber())
        {
          passenger.book(flightmap[number]);
        }
        else cout<<"The Flight not exist!\n";
        break;
      }
      case 4:
      {
        cout<<"Please input the flight number:\n";
        string number;
        cin>>number;
        passenger.refund(flightmap[number]);
        break;
      }
      case 5:
      {
        showAll();
        break;
      }
      case 6:
      {
        passenger.showMyTicket();
        break;
      }
      case 0:service="0"; break;
      default:  cout<<"Unuseful code! Please input corresponding service code again:\n";
                cin>>service;
                goto temp2;
    }
    }
  }
   void admin()
   {  
      int n;
      Flight f;
      //cout<<f.getStatus()<<endl;
      cout<<"How many flight do you want to add? Please input the number:\n";
      cin>>n;
      cout<<"Add flight message format like this:\n";
      showTheMessage(1); 
      cout<<"xh570     278  Fuzhou    Peiking   2021/01/31/22:00    2021/02/01/02:00    Sunday    \n";
      ofstream out;
      out.open(fileName,ios::app|ios::app);
      for(int i=0;i<n;i++)
      {
        cin>>f;
        flightmap[f.getFlightNumber()]=f;
        out<<f<<endl;
      }
      out.close();
   }
   void findByNumber(string number)
   { 
     if(flightmap[number].getFlightNumber()==number)
     {
     showTheMessage();
     cout<<flightmap[number]<<endl;
     }
     else cout<<"This flight NOT exist!\n";
   }
   void findByEndStation(string station)
   {
     int flag=0;
     for(auto i:flightmap)
     {
       if(i.second.getEndStation()==station&&flag==0)
       {
        showTheMessage();
        flag=1;
       }
       if(i.second.getEndStation()==station&&flag==1)
       {
         cout<<i.second<<endl;
       }
     }
     if(flag==0)cout<<"Such flights NOT exist!\n";
   } 
   void showAll()
   {
    showTheMessage();
        /* xh570 278 Fuzhou Peiking 2021/01/31/22:00 2021/02/01/02:00 Sunday Bookable*/
    for(auto i:flightmap)
    {
      cout<<i.second<<endl;
    }
   }
   public:
   ~Menu()
   { 
    ofstream out;
    out.open(fileName,ios::out|ios::trunc);
    for(auto i:flightmap)out<<i.second<<endl;
    out.close();
   // for(auto i:flightmap)cout<<i.second<<endl;
   }
}; 
int  main()
{
  Menu menu;
  Passenger passenger;
  menu.mainMenu(passenger);
  system("pause");
  return 0;
  string a = "145313";
 
}